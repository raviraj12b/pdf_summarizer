"""
Frontend Package
File: frontend/__init__.py
Description: Frontend module for UI components and styling
"""

from .styles import load_custom_css
from .components import (
    render_header,
    render_features,
    render_sidebar,
    render_file_info,
    render_text_statistics,
    render_processing_status,
    render_summary_statistics,
    render_summary_display,
    render_download_section,
    render_footer
)

__all__ = [
    'load_custom_css',
    'render_header',
    'render_features',
    'render_sidebar',
    'render_file_info',
    'render_text_statistics',
    'render_processing_status',
    'render_summary_statistics',
    'render_summary_display',
    'render_download_section',
    'render_footer'
]
