# =============================================================
# SUPABASE CLIENT — shared connection for all database modules
# =============================================================
# Uses @st.cache_resource to maintain a single client per process.
# Reads credentials from Streamlit secrets (cloud) or .env (local).
# =============================================================

import os
import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase() -> Client:
    """Return a cached Supabase client instance."""
    url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError(
            "Missing SUPABASE_URL or SUPABASE_KEY. "
            "Add them to .env (local) or Streamlit secrets (cloud)."
        )
    return create_client(url, key)
