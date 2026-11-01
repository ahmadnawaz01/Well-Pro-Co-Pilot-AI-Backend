from typing import Any, Dict, List, Optional, Union
import httpx
from fastapi import HTTPException, status
from app.core.config import settings


class FrappeClient:
    """
    Centralized HTTP client for communicating with Frappe WellPro Backend RPC endpoints.
    Handles authentication headers, standard Frappe response envelopes, and error mapping.
    """

    @staticmethod
    def _get_headers(token: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if token:
            clean_token = token if token.startswith("token ") else f"token {token}"
            headers["Authorization"] = clean_token
        return headers

    @staticmethod
    def _unwrap_response(response: httpx.Response) -> Dict[str, Any]:
        """
        Frappe wraps successful returns in {"message": ...}.
        Unwraps and returns the inner dictionary or payload.
        """
        try:
            res_json = response.json()
        except Exception:
            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Frappe error ({response.status_code}): {response.text}",
                )
            return {"raw": response.text}

        if response.status_code >= 400:
            error_msg = (
                res_json.get("message")
                or res_json.get("exception")
                or res_json.get("_server_messages")
                or response.text
            )
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Frappe error ({response.status_code}): {error_msg}",
            )

        if "message" in res_json:
            return res_json["message"]
        return res_json

    @classmethod
    async def _post(
        cls,
        method_name: str,
        data: Optional[Dict[str, Any]] = None,
        token: Optional[str] = None,
        timeout: float = 15.0,
    ) -> Dict[str, Any]:
        url = f"{settings.FRAPPE_BASE_URL}/api/method/well_pro.well_pro_app.api.{method_name}"
        headers = cls._get_headers(token)

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(url, json=data or {}, headers=headers)
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Unable to connect to Frappe service at {url}: {str(exc)}",
                )

        return cls._unwrap_response(response)

    @classmethod
    async def _get(
        cls,
        method_name: str,
        params: Optional[Dict[str, Any]] = None,
        token: Optional[str] = None,
        timeout: float = 15.0,
    ) -> Dict[str, Any]:
        url = f"{settings.FRAPPE_BASE_URL}/api/method/well_pro.well_pro_app.api.{method_name}"
        headers = cls._get_headers(token)

        # Remove None values from params
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.get(url, params=clean_params, headers=headers)
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Unable to connect to Frappe service at {url}: {str(exc)}",
                )

        return cls._unwrap_response(response)

    # ---------------- 5.1 Authentication ----------------

    @classmethod
    async def signup(
        cls,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "email": email,
            "password": password,
            "first_name": first_name or "",
            "last_name": last_name or "",
        }
        return await cls._post("signup", data=payload)

    @classmethod
    async def login(cls, usr: str, pwd: str) -> Dict[str, Any]:
        payload = {"usr": usr, "pwd": pwd}
        return await cls._post("login", data=payload)

    @classmethod
    async def verify_user_session(cls, token: str) -> Dict[str, Any]:
        return await cls._get("verify_user_session", token=token)

    # ---------------- 5.2 Data Ingestion & Creation ----------------

    @classmethod
    async def insert_record(
        cls,
        payload: Union[Dict[str, Any], List[Dict[str, Any]]],
        token: str,
    ) -> Dict[str, Any]:
        """
        Calls Frappe insert_record.
        Accepts:
        - Format A: Multi-DocType dictionary
        - Format B: Single record dict
        - Format C: Batch array or {"records": [...]}
        """
        url = f"{settings.FRAPPE_BASE_URL}/api/method/well_pro.well_pro_app.api.insert_record"
        headers = cls._get_headers(token)

        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Unable to connect to Frappe service at {url}: {str(exc)}",
                )

        return cls._unwrap_response(response)

    @classmethod
    async def store_ai_record(
        cls,
        payload: Dict[str, Any],
        token: str,
    ) -> Dict[str, Any]:
        """
        Calls Frappe store_ai_record.
        Accepts domain keyed dict: {"health": {...}, "financial": [...], "social": {...}, "wellbeing": {...}}
        """
        return await cls._post("store_ai_record", data=payload, token=token, timeout=20.0)

    # ---------------- 5.3 Record Modification & Eviction ----------------

    @classmethod
    async def update_record(
        cls,
        doctype: str,
        name: str,
        update_data: Dict[str, Any],
        token: str,
    ) -> Dict[str, Any]:
        payload = {
            "doctype": doctype,
            "name": name,
            "update_data": update_data,
        }
        return await cls._post("update_record", data=payload, token=token)

    @classmethod
    async def delete_record(
        cls,
        doctype: str,
        name: str,
        token: str,
    ) -> Dict[str, Any]:
        payload = {
            "doctype": doctype,
            "name": name,
        }
        return await cls._post("delete_record", data=payload, token=token)

    # ---------------- 5.4 Data Querying & Retrieval ----------------

    @classmethod
    async def get_user_records(
        cls,
        doctype: str,
        token: str,
        limit: int = 50,
        offset: int = 0,
        order_by: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {
            "doctype": doctype,
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "from_date": from_date,
            "to_date": to_date,
        }
        return await cls._get("get_user_records", params=params, token=token)

    # ---------------- 5.5 Dashboard & Score Analytics ----------------

    @classmethod
    async def get_dashboard_metrics(
        cls,
        token: str,
        days: int = 30,
        as_of_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {
            "days": days,
            "as_of_date": as_of_date,
        }
        return await cls._get("get_dashboard_metrics", params=params, token=token)

    @classmethod
    async def recalculate_score(
        cls,
        date: Optional[str],
        token: str,
    ) -> Dict[str, Any]:
        payload = {"date": date} if date else {}
        return await cls._post("recalculate_score", data=payload, token=token)

    # ---------------- 5.6 Scoring Goals Configuration ----------------

    @classmethod
    async def setup_scoring_goals(
        cls,
        goals: Dict[str, Any],
        recalculate: bool,
        token: str,
    ) -> Dict[str, Any]:
        payload = {
            "goals": goals,
            "recalculate": recalculate,
        }
        return await cls._post("setup_scoring_goals", data=payload, token=token)

    @classmethod
    async def get_scoring_goals(cls, token: str) -> Dict[str, Any]:
        return await cls._get("get_scoring_goals", token=token)

