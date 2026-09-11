"""
=====================================================

TalentAI OS

Embedded Systems Technology Catalog

Official technologies for Embedded Software,
Linux platforms and connected devices.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from app.intelligence.domain.technology import Technology


EMBEDDED_TECHNOLOGIES = {

    # =====================================================
    # EMBEDDED SOFTWARE
    # =====================================================

    "Embedded Software": Technology(
        name="Embedded Software",
        vendor="Generic",
        category="Embedded Systems",
        aliases=[
            "embedded software development",
            "embedded systems",
            "embedded development"
        ]
    ),

    # =====================================================
    # EMBEDDED LINUX
    # =====================================================

    "Embedded Linux": Technology(
        name="Embedded Linux",
        vendor="Linux",
        category="Embedded Systems",
        aliases=[
            "embedded linux",
            "arm linux",
            "linux embedded"
        ]
    ),

    # =====================================================
    # LINUX KERNEL
    # =====================================================

    "Linux Kernel": Technology(
        name="Linux Kernel",
        vendor="Linux",
        category="Operating System",
        aliases=[
            "linux kernel",
            "kernel linux"
        ]
    ),

    # =====================================================
    # ANDROID
    # =====================================================

    "Android": Technology(
        name="Android",
        vendor="Google",
        category="Operating System",
        aliases=[
            "android",
            "android tv",
            "androidtv"
        ]
    ),

    # =====================================================
    # C
    # =====================================================

    "C": Technology(
        name="C",
        vendor="Generic",
        category="Programming Language",
        aliases=[]
    ),

    # =====================================================
    # C++
    # =====================================================

    "C++": Technology(
        name="C++",
        vendor="Generic",
        category="Programming Language",
        aliases=[
            "cplusplus",
            "cpp"
        ]
    ),

    # =====================================================
    # MPEG
    # =====================================================

    "MPEG": Technology(
        name="MPEG",
        vendor="Generic",
        category="Multimedia",
        aliases=[
            "mpeg",
            "mpeg-ts",
            "mpeg ts"
        ]
    ),

    # =====================================================
    # WI-FI
    # =====================================================

    "Wi-Fi": Technology(
        name="Wi-Fi",
        vendor="Generic",
        category="Networking",
        aliases=[
            "wifi",
            "wi-fi"
        ]
    ),

    # =====================================================
    # FIRMWARE
    # =====================================================

    "Firmware": Technology(
        name="Firmware",
        vendor="Generic",
        category="Embedded Systems",
        aliases=[
            "firmware"
        ]
    ),

    # =====================================================
    # MIDDLEWARE
    # =====================================================

    "Middleware": Technology(
        name="Middleware",
        vendor="Generic",
        category="Software Architecture",
        aliases=[
            "middleware"
        ]
    ),

    # =====================================================
    # IPC
    # =====================================================

    "IPC": Technology(
        name="IPC",
        vendor="Generic",
        category="Operating System",
        aliases=[
            "inter-process communication",
            "inter process communication"
        ]
    ),

    # =====================================================
    # NETWORKING
    # =====================================================

    "Networking": Technology(
        name="Networking",
        vendor="Generic",
        category="Networking",
        aliases=[
            "networking",
            "network components",
            "networking components",
            "tcp/ip",
            "tcp",
            "ip",
            "dns",
            "dhcp",
            "snmp"
        ]
    ),

}