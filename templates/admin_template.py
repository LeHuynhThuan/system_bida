# Admin Dashboard HTML Template

admin_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <title>Bida Club - Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            color: #e0e0e0;
            overflow-x: hidden;
        }

        /* === HEADER === */
        .header {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255,255,255,0.08);
            padding: 16px 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .logo-icon {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 4px 15px rgba(99,102,241,0.4);
        }

        .header-title {
            font-size: 20px;
            font-weight: 700;
            background: linear-gradient(90deg, #c4b5fd, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }

        .header-sub {
            font-size: 12px;
            color: #9ca3af;
            font-weight: 400;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 20px;
        }

        /* === STATS BAR === */
        .stats-bar {
            display: flex;
            gap: 16px;
            align-items: center;
        }

        .stat-chip {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 6px 16px;
            font-size: 13px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.3s ease;
        }

        .stat-chip .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            animation: pulse-dot 2s infinite;
        }

        .dot-green { background: #22c55e; box-shadow: 0 0 8px #22c55e; }
        .dot-red { background: #ef4444; box-shadow: 0 0 8px #ef4444; }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.8); }
        }

        #clock {
            font-size: 14px;
            font-weight: 600;
            color: #a5b4fc;
            font-variant-numeric: tabular-nums;
        }

        /* === STATUS BANNER === */
        .status-banner {
            margin: 20px 30px 0;
            padding: 14px 24px;
            border-radius: 14px;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.5s ease;
        }

        .status-connecting {
            background: rgba(59,130,246,0.15);
            border: 1px solid rgba(59,130,246,0.3);
            color: #93c5fd;
        }

        .status-connected {
            background: rgba(34,197,94,0.15);
            border: 1px solid rgba(34,197,94,0.3);
            color: #86efac;
        }

        .status-error {
            background: rgba(239,68,68,0.15);
            border: 1px solid rgba(239,68,68,0.3);
            color: #fca5a5;
        }

        /* === MAIN CONTENT (2-COLUMN GRID) === */
        .main-content {
            padding: 20px 30px;
            max-width: 1600px;
            margin: 0 auto;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 30px;
        }

        .dashboard-col {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .section-label {
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #8b949e;
            margin-bottom: 8px;
        }

        /* === TABLES GRID === */
        .tables-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }

        .cameras-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }

        .table-card {
            background: rgba(255,255,255,0.04);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .table-card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
            border-color: rgba(255,255,255,0.15);
        }

        .table-card.playing {
            border-color: rgba(99,102,241,0.6);
            background: rgba(99,102,241,0.06);
            box-shadow: 0 8px 30px rgba(99,102,241,0.2), inset 0 0 15px rgba(99,102,241,0.1);
        }

        .table-card.playing:hover {
            box-shadow: 0 15px 40px rgba(99,102,241,0.3), inset 0 0 20px rgba(99,102,241,0.15);
            border-color: rgba(99,102,241,0.8);
        }

        .table-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .table-name {
            font-size: 17px;
            font-weight: 800;
            color: white;
        }

        .table-badges {
            display: flex;
            gap: 6px;
        }

        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .badge-vip {
            background: linear-gradient(135deg, #fbbf24, #d97706, #fbbf24);
            background-size: 200% 200%;
            animation: gradientMove 3s ease infinite;
            color: #1e1b4b;
            font-size: 10px;
            font-weight: 800;
            padding: 2px 6px;
            border-radius: 4px;
            text-transform: uppercase;
        }

        .badge-std {
            background: rgba(255,255,255,0.1);
            color: #e5e7eb;
            font-size: 10px;
            font-weight: 600;
            padding: 2px 6px;
            border-radius: 4px;
            text-transform: uppercase;
        }

        .badge-type {
            background: rgba(99,102,241,0.2);
            color: #a5b4fc;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
            text-transform: uppercase;
        }

        .table-status-label {
            font-size: 12px;
            font-weight: 700;
        }

        .status-empty { color: #9ca3af; }
        .status-playing { color: #86efac; animation: pulse-text 2s infinite; }

        @keyframes pulse-text {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        .table-details {
            font-size: 12px;
            color: #9ca3af;
            line-height: 1.6;
            background: rgba(0,0,0,0.25);
            padding: 12px;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            border: 1px solid rgba(255,255,255,0.03);
        }

        .order-btn-group {
            display: flex;
            gap: 8px;
            margin-top: 4px;
            flex-wrap: wrap;
        }

        /* === CARD BASE === */
        .card {
            background: rgba(255,255,255,0.04);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }

        .card-header-title {
            font-size: 16px;
            font-weight: 700;
            color: #c4b5fd;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* === LIVE CAM STYLING === */
        .live-stream-container {
            position: relative;
            width: 100%;
            aspect-ratio: 16/9;
            background: #000;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.08);
        }

        .live-stream-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .live-tag {
            position: absolute;
            top: 12px;
            left: 12px;
            background: #ef4444;
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            animation: blink 1.5s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* === HIGHLIGHT STYLING === */
        .highlight-desc {
            font-size: 13px;
            color: #9ca3af;
            margin-bottom: 16px;
            line-height: 1.5;
        }

        .highlight-status {
            font-size: 13px;
            font-weight: 600;
            padding: 10px 16px;
            border-radius: 10px;
            margin-top: 12px;
            display: none;
        }

        .highlight-processing {
            background: rgba(59,130,246,0.15);
            color: #93c5fd;
            border: 1px solid rgba(59,130,246,0.3);
        }

        .highlight-ready {
            background: rgba(34,197,94,0.15);
            color: #86efac;
            border: 1px solid rgba(34,197,94,0.3);
        }

        .clips-list {
            margin-top: 16px;
        }

        .clip-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 14px;
            background: rgba(255,255,255,0.04);
            border-radius: 10px;
            margin-bottom: 8px;
            font-size: 13px;
        }

        .clip-item-name {
            color: #e5e7eb;
            font-weight: 500;
        }

        .clip-item-size {
            color: #8b949e;
            font-size: 12px;
        }

        /* === EVENT CARDS === */
        .event-card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            animation: slideIn 0.4s ease-out;
            transition: all 0.3s ease;
        }

        .event-card:hover {
            background: rgba(255,255,255,0.08);
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        }

        .event-card.urgent {
            border-left: 4px solid #f59e0b;
            box-shadow: 0 0 20px rgba(245,158,11,0.15);
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px) scale(0.97); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        .event-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }

        .event-badge {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 4px 10px;
            border-radius: 6px;
        }

        .badge-hand {
            background: rgba(245,158,11,0.2);
            color: #fbbf24;
            border: 1px solid rgba(245,158,11,0.3);
        }

        .badge-motion {
            background: rgba(59,130,246,0.2);
            color: #93c5fd;
            border: 1px solid rgba(59,130,246,0.3);
        }

        .event-time {
            font-size: 12px;
            color: #8b949e;
            font-variant-numeric: tabular-nums;
        }

        .event-message {
            font-size: 15px;
            font-weight: 500;
            color: #e5e7eb;
            margin-bottom: 14px;
            line-height: 1.5;
        }

        .event-image {
            width: 100%;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 16px;
        }

        .event-actions {
            display: flex;
            gap: 10px;
        }

        /* === BUTTONS === */
        .btn {
            border: none;
            padding: 10px 22px;
            border-radius: 10px;
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .btn-confirm {
            background: linear-gradient(135deg, #22c55e, #16a34a, #22c55e);
            background-size: 200% 200%;
            animation: gradientMove 4s ease infinite;
            color: white;
            box-shadow: 0 4px 12px rgba(34,197,94,0.3);
        }

        .btn-confirm:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(34,197,94,0.5); }
        .btn-confirm:active { transform: translateY(0) scale(0.96); }

        .btn-dismiss {
            background: rgba(239,68,68,0.15);
            color: #fca5a5;
            border: 1px solid rgba(239,68,68,0.2);
        }

        .btn-dismiss:hover { background: rgba(239,68,68,0.25); transform: translateY(-2px); }

        .btn-highlight {
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            color: white;
            box-shadow: 0 4px 12px rgba(99,102,241,0.3);
        }

        .btn-highlight:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(99,102,241,0.4); }

        .btn-download {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
            box-shadow: 0 4px 12px rgba(245,158,11,0.3);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn-download:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(245,158,11,0.4); }

        .btn-small {
            padding: 6px 12px !important;
            font-size: 11px !important;
            border-radius: 6px !important;
        }

        .btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            transform: none !important;
        }

        .event-resolved {
            font-size: 12px;
            font-weight: 600;
            margin-top: 8px;
            padding: 6px 12px;
            border-radius: 8px;
            display: inline-block;
        }

        .resolved-confirmed {
            background: rgba(34,197,94,0.15);
            color: #86efac;
        }

        .resolved-dismissed {
            background: rgba(239,68,68,0.15);
            color: #fca5a5;
        }

        /* === TIME MACHINE STYLING === */
        .time-machine-container {
            border-top: 1px solid rgba(255,255,255,0.08);
            padding-top: 20px;
            margin-top: 20px;
        }

        .time-machine-title {
            font-size: 14px;
            font-weight: 700;
            color: #a5b4fc;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .time-machine-row {
            display: flex;
            gap: 12px;
            align-items: center;
        }

        .time-input {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: white;
            padding: 9px 12px;
            font-family: inherit;
            font-size: 13px;
            outline: none;
            flex: 1;
        }

        /* === EMPTY STATE === */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #6b7280;
        }

        .empty-icon {
            font-size: 48px;
            margin-bottom: 16px;
            opacity: 0.5;
        }

        .empty-text {
            font-size: 15px;
            font-weight: 500;
        }

        .empty-sub {
            font-size: 13px;
            margin-top: 6px;
            color: #4b5563;
        }

        /* === SOUND TOGGLE === */
        .sound-toggle {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 10px;
            padding: 8px 14px;
            color: #e0e0e0;
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .sound-toggle:hover { background: rgba(255,255,255,0.12); }
        .sound-toggle.active { background: rgba(99,102,241,0.2); border-color: rgba(99,102,241,0.4); color: #a5b4fc; }

        /* === HAMBURGER BUTTON === */
        .menu-toggle-btn {
            background: none;
            border: none;
            color: #c4b5fd;
            font-size: 26px;
            cursor: pointer;
            padding: 4px 10px;
            border-radius: 8px;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
        }

        .menu-toggle-btn:hover {
            background: rgba(255,255,255,0.08);
            color: white;
        }

        /* === LAYOUT WITH SIDEBAR === */
        .app-container {
            display: flex;
            min-height: calc(100vh - 75px);
            position: relative;
        }

        .sidebar {
            width: 260px;
            background: rgba(15,12,41,0.6);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border-right: 1px solid rgba(255,255,255,0.08);
            padding: 30px 20px;
            display: flex;
            flex-direction: column;
            gap: 24px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 90;
        }

        .sidebar.collapsed {
            width: 0;
            padding: 30px 0;
            overflow: hidden;
            border-right: none;
            opacity: 0;
            pointer-events: none;
        }

        .sidebar-section {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .sidebar-section-title {
            font-size: 11px;
            font-weight: 700;
            color: #8b949e;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
            padding-left: 12px;
        }

        .sidebar-link {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #9ca3af;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            padding: 12px 16px;
            border-radius: 12px;
            transition: all 0.2s;
            border: 1px solid transparent;
        }

        .sidebar-link:hover {
            background: rgba(255,255,255,0.06);
            color: white;
        }

        .sidebar-link.active {
            background: rgba(99,102,241,0.15);
            border: 1px solid rgba(99,102,241,0.3);
            color: #a5b4fc;
        }

        /* === MAIN CONTENT WRAPPER === */
        .main-content-wrapper {
            flex: 1;
            padding: 24px 30px;
            transition: all 0.3s ease;
            overflow-x: hidden;
        }

        /* === RIGHT DRAWER (NGĂN KÉO TRƯỢT) === */
        .drawer {
            position: fixed;
            top: 0;
            right: 0;
            width: 385px;
            height: 100%;
            background: #0f0c29;
            background: linear-gradient(to bottom, #14113c, #0d0a21);
            border-left: 1px solid rgba(255,255,255,0.12);
            box-shadow: -10px 0 40px rgba(0,0,0,0.6);
            z-index: 1100;
            transform: translateX(100%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
        }

        .drawer.open {
            transform: translateX(0);
        }

        .drawer-header {
            padding: 24px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .drawer-header h3 {
            font-size: 16px;
            font-weight: 800;
            color: #fbbf24;
            margin: 0;
        }

        .drawer-close {
            background: none;
            border: none;
            color: #9ca3af;
            font-size: 22px;
            cursor: pointer;
            padding: 4px;
            transition: color 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .drawer-close:hover {
            color: white;
        }

        .drawer-body {
            flex: 1;
            padding: 24px;
            overflow-y: auto;
        }

        .drawer-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(4px);
            z-index: 1050;
            display: none;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .drawer-overlay.open {
            display: block;
            opacity: 1;
        }

        /* === LIVE CAMERA STREAMS GRID & STATE === */
        .live-stream-container {
            position: relative;
            cursor: pointer;
            overflow: hidden;
            border-radius: 12px;
            border: 2px solid rgba(255,255,255,0.08);
            transition: all 0.3s ease;
        }

        .live-stream-container.active-table {
            border-color: rgba(34,197,94,0.45);
            box-shadow: 0 0 15px rgba(34,197,94,0.15);
        }

        .live-stream-container.empty-table {
            border-color: rgba(156,163,175,0.15);
        }

        .stream-status-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 10px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            z-index: 10;
            letter-spacing: 0.5px;
        }

        .status-active-playing {
            background: rgba(34,197,94,0.25);
            color: #4ade80;
            border: 1px solid rgba(34,197,94,0.35);
        }

        .status-empty-waiting {
            background: rgba(156,163,175,0.15);
            color: #d1d5db;
            border: 1px solid rgba(156,163,175,0.25);
        }

        .stream-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15,23,42,0.85);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            gap: 12px;
            z-index: 5;
            transition: all 0.3s ease;
        }

        .stream-overlay.hidden {
            opacity: 0;
            pointer-events: none;
        }

        .stream-action-btn {
            background: rgba(99,102,241,0.2);
            border: 1px solid rgba(99,102,241,0.4);
            color: #a5b4fc;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 700;
            transition: all 0.2s;
            cursor: pointer;
        }

        .stream-action-btn:hover {
            background: rgba(99,102,241,0.35);
            color: white;
        }

        /* Hover overlay on live stream */
        .live-stream-container:hover .hover-action-overlay {
            opacity: 1;
        }

        .hover-action-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.2s ease;
            z-index: 4;
        }

        /* === RESPONSIVE === */
        @media (max-width: 1024px) {
            .dashboard-grid { grid-template-columns: 1fr; }
            .sidebar { position: fixed; top: 75px; left: 0; height: calc(100vh - 75px); transform: translateX(-100%); }
            .sidebar.collapsed { transform: translateX(0); width: 260px; opacity: 1; pointer-events: auto; padding: 30px 20px; }
        }

        @media (max-width: 768px) {
            .header { padding: 12px 16px; flex-direction: column; gap: 12px; }
            .main-content { padding: 16px; }
            .stats-bar { flex-wrap: wrap; justify-content: center; }
            .status-banner { margin: 12px 16px 0; }
            .event-actions { flex-direction: column; }
            .btn { justify-content: center; }
            .drawer { width: 100%; }
        }
    
        /* === CUSTOM SWEETALERT-LIKE MODAL (MATCHING IMAGE 2) === */
        .custom-confirm-overlay {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(6px);
            z-index: 10000;
            display: none;
            justify-content: center;
            align-items: center;
            padding: 16px;
        }

        .custom-confirm-card {
            background: #ffffff;
            color: #1f2937;
            border-radius: 20px;
            padding: 28px 24px;
            max-width: 420px;
            width: 100%;
            text-align: center;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
            animation: modalPop 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            font-family: system-ui, -apple-system, sans-serif;
        }

        .custom-modal-icon {
            width: 76px;
            height: 76px;
            border-radius: 50%;
            border: 4px solid #f97316;
            color: #f97316;
            font-size: 40px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px auto;
            line-height: 1;
        }

        .custom-modal-icon.info {
            border-color: #3b82f6;
            color: #3b82f6;
        }

        .custom-modal-title {
            font-size: 21px;
            font-weight: 800;
            color: #111827;
            margin: 0 0 6px 0;
        }

        .custom-modal-sub {
            font-size: 14px;
            color: #4b5563;
            margin: 0 0 18px 0;
            line-height: 1.4;
        }

        .custom-modal-options {
            text-align: left;
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 12px 16px;
            margin-bottom: 20px;
        }

        .custom-modal-radio {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 0;
            font-weight: 600;
            font-size: 14px;
            color: #374151;
            cursor: pointer;
        }

        .custom-modal-radio input[type="radio"] {
            width: 18px;
            height: 18px;
            accent-color: #10b981;
            cursor: pointer;
        }

        .custom-modal-input {
            width: 100%;
            height: 38px;
            background: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 0 12px;
            font-size: 13px;
            color: #1f2937;
            margin-top: 8px;
            outline: none;
            box-sizing: border-box;
        }

        .custom-modal-input:focus {
            border-color: #10b981;
            box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
        }

        .custom-modal-select {
            width: 100%;
            height: 42px;
            background: #ffffff;
            border: 1.5px solid #d1d5db;
            border-radius: 10px;
            padding: 0 12px;
            font-size: 14px;
            font-weight: 600;
            color: #1f2937;
            outline: none;
            box-sizing: border-box;
        }

        .custom-modal-select:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }

        .custom-modal-btns {
            display: flex;
            justify-content: center;
            gap: 12px;
        }

        .btn-custom-confirm {
            flex: 1;
            max-width: 140px;
            height: 44px;
            background: #10b981;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
        }

        .btn-custom-confirm:hover {
            background: #059669;
            transform: translateY(-1px);
        }

        .btn-custom-cancel {
            flex: 1;
            max-width: 140px;
            height: 44px;
            background: #ef4444;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
        }

        .btn-custom-cancel:hover {
            background: #dc2626;
            transform: translateY(-1px);
        }

        /* Notification Bell & Drawer - Position 2 Top Right */
        .notif-bell-btn {
            position: relative;
            background: linear-gradient(135deg, rgba(251, 191, 36, 0.25), rgba(245, 158, 11, 0.42));
            border: 2px solid #fbbf24;
            color: #fbbf24;
            font-size: 32px;
            width: 62px;
            height: 62px;
            border-radius: 18px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(245, 158, 11, 0.4);
            flex-shrink: 0;
            margin-top: 8px;
        }

        .notif-bell-btn:hover {
            background: linear-gradient(135deg, rgba(251, 191, 36, 0.45), rgba(245, 158, 11, 0.65));
            transform: scale(1.08);
            border-color: #ffffff;
            box-shadow: 0 6px 25px rgba(251, 191, 36, 0.6);
        }

        .notif-bell-btn:active {
            transform: scale(0.94);
        }

        .notif-count-badge {
            position: absolute;
            top: -7px;
            right: -7px;
            background: #ef4444;
            color: white;
            font-size: 13px;
            font-weight: 900;
            padding: 3px 9px;
            border-radius: 12px;
            border: 2px solid #0f0c29;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.9);
            line-height: 1;
        }
    </style>
</head>
<body>
    <!-- HEADER -->
    <div class="header">
        <div class="header-left">
            <button class="menu-toggle-btn" id="menu-btn" onclick="toggleSidebar()">☰</button>
            <div class="logo-icon">8</div>
            <div>
                <div class="header-title">Bida Club</div>
                <div class="header-sub">Đẳng cấp từng cú cơ</div>
                <div style="font-size: 11px; color: #8b949e; margin-top: 4px;">📍 3xx Huỳnh Tấn Phát quận 7 HCM &nbsp;|&nbsp; 📞 0396123456</div>
            </div>
        </div>
        <div class="header-right">
            <div class="stats-bar">
                <div class="stat-chip">
                    <span class="dot dot-green" id="status-dot"></span>
                    <span id="status-label">Dang ket noi...</span>
                </div>
                <div class="stat-chip">
                    <span id="event-count">0</span> su kien
                </div>
                <div id="clock">--:--:--</div>
            </div>
            <button class="sound-toggle" id="sound-btn" onclick="toggleSound()">
                <span id="sound-icon">&#128264;</span> Am thanh
            </button>
        </div>
    </div>

    <!-- STATUS BANNER -->
    <div class="status-banner status-connecting" id="status-banner">
        <span id="banner-icon">&#9881;</span>
        <span id="banner-text">Dang khoi tao ket noi toi AI Camera Server...</span>
    </div>

    <!-- APP CONTAINER -->
    <div class="app-container">
        <!-- LEFT SIDEBAR -->
        <div class="sidebar" id="sidebar">
            <div class="sidebar-section">
                <div class="sidebar-section-title">🎱 QUẢN LÝ BÀN</div>
                <a href="#" class="sidebar-link active" id="filter-all" onclick="setTableFilter('all', this)">📋 Tất cả bàn bida</a>
                <a href="#" class="sidebar-link" id="filter-empty" onclick="setTableFilter('empty', this)">🟢 Danh sách bàn trống</a>
                <a href="#" class="sidebar-link" id="filter-playing" onclick="setTableFilter('playing', this)">🔴 Bàn đang chơi</a>
            </div>
            
            <div class="sidebar-section" style="border-top: 1px solid rgba(255,255,255,0.06); padding-top: 20px;">
                <div class="sidebar-section-title">🎥 CÔNG CỤ CAMERA</div>
                <a href="#" class="sidebar-link" onclick="toggleDrawer(true)">⏳ Trích xuất Highlight</a>
            </div>
            
            <div class="sidebar-section" style="border-top: 1px solid rgba(255,255,255,0.06); padding-top: 20px;">
                <div class="sidebar-section-title">📦 KHO HÀNG & THỰC ĐƠN</div>
                <a href="#" class="sidebar-link" onclick="openInventoryModal()">📦 Quản lý Kho & Thực đơn</a>
            </div>
            
            <div class="sidebar-section" style="border-top: 1px solid rgba(255,255,255,0.06); padding-top: 20px;">
                <div class="sidebar-section-title">📊 BÁO CÁO & LỊCH SỬ</div>
                <a href="#" class="sidebar-link" onclick="openReportModal()">📊 Xuất báo cáo Doanh thu</a>
                <a href="#" class="sidebar-link" onclick="openHistoryModal()">🕰️ Lịch sử Bàn chơi</a>
            </div>
        </div>

        <!-- MAIN CONTENT WRAPPER -->
        <div class="main-content-wrapper">
            <!-- MAIN -->
            <div class="main-content">
                <div class="dashboard-grid">
                    <!-- LEFT COLUMN: TABLES & LIVE CAM FEED -->
                    <div class="dashboard-col">
                        <!-- BILLIARD TABLES SECTION (MỚI) -->
                        <div class="card">
                            <div class="card-header-title">🎱 Danh sách quản lý bàn bida</div>
                            <div class="tables-grid" id="tables-grid">
                                <!-- Danh sách bàn bida load động qua JS -->
                            </div>
                        </div>

                        <!-- LIVE CAMERA FEED GRID 2x2 -->
                        <div class="card">
                            <div class="card-header-title">🎥 Live Camera Streams - Hệ thống giám sát bàn chơi</div>
                            <div class="cameras-grid">
                                <div class="live-stream-container" id="cam-container-1" onclick="toggleCamStream(1)">
                                    <div class="live-tag" style="font-size: 10px; padding: 2px 6px;">Bàn 1</div>
                                    <div class="stream-status-badge status-empty-waiting" id="cam-status-1">BÀN TRỐNG</div>
                                    <img id="live-cam-1" class="live-stream-img" src="" onerror="this.src='https://images.unsplash.com/photo-1544197150-b99a580bb7a8?q=80&w=600&auto=format&fit=crop'" alt="Bàn 1 Cam">
                                    <div class="stream-overlay" id="cam-overlay-1">
                                        <button class="stream-action-btn">▶ Xem Stream</button>
                                    </div>
                                    <div class="hover-action-overlay" id="cam-hover-1">
                                        <button class="stream-action-btn" style="background: rgba(239,68,68,0.25); border-color: rgba(239,68,68,0.4); color: #fca5a5;">⏸ Tắt Stream</button>
                                    </div>
                                </div>
                                <div class="live-stream-container" id="cam-container-2" onclick="toggleCamStream(2)">
                                    <div class="live-tag" style="font-size: 10px; padding: 2px 6px; background: #6366f1;">Bàn 2</div>
                                    <div class="stream-status-badge status-empty-waiting" id="cam-status-2">BÀN TRỐNG</div>
                                    <img id="live-cam-2" class="live-stream-img" src="" onerror="this.src='https://images.unsplash.com/photo-1544197150-b99a580bb7a8?q=80&w=600&auto=format&fit=crop'" alt="Bàn 2 Cam">
                                    <div class="stream-overlay" id="cam-overlay-2">
                                        <button class="stream-action-btn">▶ Xem Stream</button>
                                    </div>
                                    <div class="hover-action-overlay" id="cam-hover-2">
                                        <button class="stream-action-btn" style="background: rgba(239,68,68,0.25); border-color: rgba(239,68,68,0.4); color: #fca5a5;">⏸ Tắt Stream</button>
                                    </div>
                                </div>
                                <div class="live-stream-container" id="cam-container-3" onclick="toggleCamStream(3)">
                                    <div class="live-tag" style="font-size: 10px; padding: 2px 6px; background: #8b5cf6;">Bàn 3</div>
                                    <div class="stream-status-badge status-empty-waiting" id="cam-status-3">BÀN TRỐNG</div>
                                    <img id="live-cam-3" class="live-stream-img" src="" onerror="this.src='https://images.unsplash.com/photo-1544197150-b99a580bb7a8?q=80&w=600&auto=format&fit=crop'" alt="Bàn 3 Cam">
                                    <div class="stream-overlay" id="cam-overlay-3">
                                        <button class="stream-action-btn">▶ Xem Stream</button>
                                    </div>
                                    <div class="hover-action-overlay" id="cam-hover-3">
                                        <button class="stream-action-btn" style="background: rgba(239,68,68,0.25); border-color: rgba(239,68,68,0.4); color: #fca5a5;">⏸ Tắt Stream</button>
                                    </div>
                                </div>
                                <div class="live-stream-container" id="cam-container-4" onclick="toggleCamStream(4)">
                                    <div class="live-tag" style="font-size: 10px; padding: 2px 6px; background: #ec4899;">Bàn 4</div>
                                    <div class="stream-status-badge status-empty-waiting" id="cam-status-4">BÀN TRỐNG</div>
                                    <img id="live-cam-4" class="live-stream-img" src="" onerror="this.src='https://images.unsplash.com/photo-1544197150-b99a580bb7a8?q=80&w=600&auto=format&fit=crop'" alt="Bàn 4 Cam">
                                    <div class="stream-overlay" id="cam-overlay-4">
                                        <button class="stream-action-btn">▶ Xem Stream</button>
                                    </div>
                                    <div class="hover-action-overlay" id="cam-hover-4">
                                        <button class="stream-action-btn" style="background: rgba(239,68,68,0.25); border-color: rgba(239,68,68,0.4); color: #fca5a5;">⏸ Tắt Stream</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- RIGHT COLUMN: REALTIME ALERTS LOG -->
                    <div class="dashboard-col">
                        <div class="section-label">Canh bao realtime</div>
                        <div id="events">
                            <div class="empty-state" id="empty-state">
                                <div class="empty-icon">&#128247;</div>
                                <div class="empty-text">Chua co su kien nao</div>
                                <div class="empty-sub">He thong dang cho AI Camera gui du lieu...</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- RIGHT HIGHLIGHT DRAWER -->
    <div class="drawer-overlay" id="drawer-overlay" onclick="toggleDrawer(false)"></div>
    <div class="drawer" id="highlight-drawer">
        <div class="drawer-header">
            <h3>🎬 Highlight Clip Center</h3>
            <button class="drawer-close" onclick="toggleDrawer(false)">✕</button>
        </div>
        <div class="drawer-body">
            <div class="highlight-desc" style="font-size: 13px; color: #9ca3af; line-height: 1.5; margin-bottom: 20px;">
                Chọn bàn bida bên dưới, sau đó bấm cắt nhanh 30 giây vừa qua.
                Hoặc trích xuất video trong quá khứ qua Cỗ Máy Thời Gian (lưu tối đa 30 phút).
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 6px; margin-bottom: 20px;">
                <span style="font-size: 13px; font-weight: 600; color: #a5b4fc;">Chọn bàn cần trích xuất:</span>
                <select id="highlight-table-select" style="background:#1f1b4b; border:1px solid rgba(255,255,255,0.15); border-radius:8px; color:white; padding:8px 12px; font-size:13px; font-weight:700; outline:none; cursor: pointer; width: 100%;">
                    <option value="1">Bàn 1</option>
                    <option value="2">Bàn 2</option>
                    <option value="3">Bàn 3</option>
                    <option value="4">Bàn 4</option>
                </select>
            </div>
            
            <button class="btn btn-highlight" id="clip-btn" onclick="requestSelectedClip()" style="width: 100%; justify-content: center; margin-bottom: 20px;">🎥 Highlight 30s bàn đã chọn</button>

            <!-- TIME MACHINE -->
            <div class="time-machine-container">
                <div class="time-machine-title">⏳ Co May Thoi Gian</div>
                <div class="time-machine-row" style="margin-top: 10px;">
                    <input type="time" id="time-input" class="time-input">
                    <button class="btn btn-download" style="padding: 10px 18px;" id="past-clip-btn" onclick="requestSelectedPastClip()">⌛ Trích xuất</button>
                </div>
            </div>

            <div class="highlight-status" id="clip-status" style="margin-top: 20px; display: none;"></div>
            <div class="clips-list" id="clips-list" style="margin-top: 20px;"></div>
        </div>
    </div>

    <!-- REPORT MODAL -->
    <div class="bill-modal-overlay" id="report-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); z-index: 1000; align-items: center; justify-content: center;">
        <div class="card" style="width: 90%; max-width: 500px; background: #1e1b4b; border: 1px solid rgba(255,255,255,0.15); display: flex; flex-direction: column; gap: 16px; padding: 24px;">
            <div style="font-size: 18px; font-weight: 800; color: #fbbf24; border-bottom: 2px dashed rgba(255,255,255,0.15); padding-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span>📊 XUẤT BÁO CÁO DOANH THU</span>
                </div>
                <span style="cursor: pointer; color: #9ca3af; font-size: 20px; font-weight: bold; padding: 4px;" onclick="closeReportModal()">✕</span>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 12px; color: white;">
                <div>
                    <label style="font-size: 13px; font-weight: 600; color: #a5b4fc; display: block; margin-bottom: 4px;">Từ ngày:</label>
                    <input type="date" id="report-start-date" style="width: 100%; height: 40px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 12px; font-size: 14px; outline: none; color-scheme: dark;">
                </div>
                <div>
                    <label style="font-size: 13px; font-weight: 600; color: #a5b4fc; display: block; margin-bottom: 4px;">Đến ngày:</label>
                    <input type="date" id="report-end-date" style="width: 100%; height: 40px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 12px; font-size: 14px; outline: none; color-scheme: dark;">
                </div>
            </div>
            
            <button onclick="downloadRevenueReport()" style="margin-top: 8px; height: 44px; border-radius: 8px; border: none; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; font-weight: bold; font-size: 15px; cursor: pointer; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">📥 Tải file Excel (.csv)</button>
        </div>
    </div>

    <!-- HISTORY MODAL -->
    <div class="bill-modal-overlay" id="history-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); z-index: 1000; align-items: center; justify-content: center;">
        <div class="card" style="width: 95%; max-width: 800px; background: #1e1b4b; border: 1px solid rgba(255,255,255,0.15); display: flex; flex-direction: column; gap: 16px; padding: 24px; max-height: 90vh; overflow-y: auto;">
            <div style="font-size: 18px; font-weight: 800; color: #fbbf24; border-bottom: 2px dashed rgba(255,255,255,0.15); padding-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span>🕰️ LỊCH SỬ BÀN CHƠI</span>
                </div>
                <span style="cursor: pointer; color: #9ca3af; font-size: 20px; font-weight: bold; padding: 4px;" onclick="closeHistoryModal()">✕</span>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #d1d5db; margin-bottom: 8px;">
                <span>* Chỉ có thể xóa các phiên chơi có thời gian kết thúc quá 48 giờ.</span>
                <button onclick="deleteSelectedHistory()" id="btn-delete-history" style="padding: 8px 16px; border-radius: 8px; border: none; background: #ef4444; color: white; font-weight: bold; cursor: pointer; transition: background 0.2s; opacity: 0.5;" disabled>🗑️ Xóa đã chọn</button>
            </div>

            <div style="max-height: 400px; overflow-y: auto; background: rgba(0,0,0,0.25); border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                <table style="width: 100%; border-collapse: collapse; font-size: 12px; text-align: left;">
                    <thead>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); color: #a5b4fc; font-weight: 700;">
                            <th style="padding: 10px 8px; width: 40px; text-align: center;">
                                <input type="checkbox" id="chk-all-history" onclick="toggleAllHistory(this)" style="cursor: pointer;">
                            </th>
                            <th style="padding: 10px 8px;">BÀN</th>
                            <th style="padding: 10px 8px;">GIỜ VÀO</th>
                            <th style="padding: 10px 8px;">GIỜ RA</th>
                            <th style="padding: 10px 8px; text-align: right;">THỜI GIAN</th>
                            <th style="padding: 10px 8px; text-align: right;">TỔNG TIỀN</th>
                            <th style="padding: 10px 8px; text-align: center; width: 80px;">CHI TIẾT</th>
                        </tr>
                    </thead>
                    <tbody id="history-items-body">
                        <!-- History data loaded via JS -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- INVENTORY MANAGEMENT MODAL -->
    <div class="bill-modal-overlay" id="inventory-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); z-index: 1000; align-items: center; justify-content: center;">
        <div class="card" style="width: 95%; max-width: 720px; background: #1e1b4b; border: 1px solid rgba(255,255,255,0.15); display: flex; flex-direction: column; gap: 16px; padding: 24px; max-height: 90vh; overflow-y: auto;">
            <div style="font-size: 18px; font-weight: 800; color: #fbbf24; border-bottom: 2px dashed rgba(255,255,255,0.15); padding-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span>📦 QUẢN LÝ KHO HÀNG & THỰC ĐƠN</span>
                </div>
                <span style="cursor: pointer; color: #9ca3af; font-size: 20px; font-weight: bold; padding: 4px;" onclick="closeInventoryModal()">✕</span>
            </div>

            <!-- Tabs Header -->
            <div style="display: flex; gap: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">
                <button id="tab-btn-products" onclick="switchInventoryTab('products')" style="padding: 8px 16px; border-radius: 8px; border: none; background: #6366f1; color: white; font-weight: bold; cursor: pointer;">🍔 Quản lý Thực đơn</button>
                <button id="tab-btn-tables" onclick="switchInventoryTab('tables')" style="padding: 8px 16px; border-radius: 8px; border: none; background: transparent; color: #9ca3af; font-weight: bold; cursor: pointer;">🎱 Quản lý Bàn Bida</button>
            </div>

            <!-- TAB: PRODUCTS -->
            <div id="tab-content-products">
                <!-- Form thêm sản phẩm mới -->
                <div style="background: rgba(255,255,255,0.04); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); display: flex; flex-direction: column; gap: 10px;">
                    <div style="font-weight: 700; color: #a5b4fc; font-size: 14px;">➕ Thêm sản phẩm mới</div>
                    <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 8px;">
                        <input type="text" id="new-prod-name" placeholder="Tên sản phẩm (Sting dâu...)" style="height: 38px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 10px; font-size: 13px; outline: none;">
                        
                        <input list="cat-list" type="text" id="new-prod-category" placeholder="Danh mục..." style="height: 38px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 10px; font-size: 13px; outline: none;">
                        <datalist id="cat-list">
                            <option value="Thức uống">
                            <option value="Đồ ăn">
                            <option value="Thuốc lá">
                            <option value="Dịch vụ khác">
                        </datalist>

                        <input type="number" id="new-prod-price" placeholder="Đơn giá (VNĐ)" style="height: 38px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 10px; font-size: 13px; outline: none;">
                        <input type="number" id="new-prod-stock" placeholder="Tồn ban đầu" style="height: 38px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 10px; font-size: 13px; outline: none;">
                    </div>
                    <input type="text" id="new-prod-image" placeholder="Link hình ảnh (Ví dụ: https://... hoặc để trống)" style="height: 38px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 10px; font-size: 13px; outline: none; margin-bottom: 4px;">
                    <button onclick="addNewProduct()" style="height: 36px; border-radius: 6px; border: none; background: linear-gradient(135deg, #10b981, #059669); color: white; font-weight: bold; cursor: pointer; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">Thêm sản phẩm</button>
                </div>

                <!-- Danh sách sản phẩm hiện tại -->
                <div style="font-size: 13px; color: #d1d5db; margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div style="font-weight: 700; color: #fbbf24; font-size: 14px;">Danh sách thực phẩm trong kho:</div>
                        <div style="display: flex; gap: 8px;">
                            <button onclick="saveAllProducts()" style="background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">💾 Lưu tất cả</button>
                            <button onclick="deleteSelectedProducts()" style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; border: none; padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">🗑️ Xóa đã chọn</button>
                        </div>
                    </div>

                    <div style="max-height: 280px; overflow-y: auto; background: rgba(0,0,0,0.25); border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                        <table style="width: 100%; border-collapse: collapse; font-size: 12px; text-align: left;">
                            <thead>
                                <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); color: #a5b4fc; font-weight: 700;">
                                    <th style="padding: 10px 8px; text-align: center; width: 34px;"><input type="checkbox" id="chk-all-prods" onchange="toggleSelectAllProds(this)" title="Chọn tất cả"></th>
                                    <th style="padding: 10px 8px;">TÊN SẢN PHẨM</th>
                                    <th style="padding: 10px 8px;">DANH MỤC</th>
                                    <th style="padding: 10px 8px;">HÌNH ẢNH</th>
                                    <th style="padding: 10px 8px; text-align: right;">ĐƠN GIÁ (VNĐ)</th>
                                    <th style="padding: 10px 8px; text-align: center;">TỒN KHO</th>
                                    <th style="padding: 10px 8px; text-align: center;">HÀNH ĐỘNG</th>
                                </tr>
                            </thead>
                            <tbody id="inventory-items-body">
                                <!-- Items listed here -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB: TABLES -->
            <div id="tab-content-tables" style="display: none;">
                <!-- Form thêm bàn mới -->
                <div style="background: rgba(255,255,255,0.04); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); display: flex; flex-direction: column; gap: 10px;">
                    <div style="font-weight: 700; color: #a5b4fc; font-size: 14px;">➕ Thêm Bàn Bida Mới</div>
                    <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 8px;">
                        <input type="text" id="new-table-name" placeholder="Tên bàn (VD: Bàn 5 Bida Lỗ)" style="height: 38px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 10px; font-size: 13px; outline: none;">
                        
                        <select id="new-table-type" style="height: 38px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 10px; font-size: 13px; outline: none;">
                            <option value="LIP">Bida Líp</option>
                            <option value="3C">Bida 3 Băng</option>
                            <option value="POOL">Bida Lỗ</option>
                        </select>

                        <select id="new-table-tier" style="height: 38px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 10px; font-size: 13px; outline: none;">
                            <option value="STANDARD">Bàn Thường</option>
                            <option value="VIP">Bàn VIP</option>
                        </select>

                        <input type="number" id="new-table-price" placeholder="Giá/giờ (VNĐ)" style="height: 38px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 10px; font-size: 13px; outline: none;">
                    </div>
                    <input type="text" id="new-table-cam" placeholder="Camera ID (0, 1, 2...) hoặc RTSP URL" style="height: 38px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white; padding: 0 10px; font-size: 13px; outline: none; margin-bottom: 4px;">
                    <button onclick="addNewAdminTable()" style="height: 36px; border-radius: 6px; border: none; background: linear-gradient(135deg, #10b981, #059669); color: white; font-weight: bold; cursor: pointer; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">Thêm Bàn</button>
                </div>

                <!-- Danh sách bàn hiện tại -->
                <div style="font-size: 13px; color: #d1d5db; margin-top: 16px;">
                    <div style="font-weight: 700; color: #fbbf24; margin-bottom: 8px;">Danh sách Bàn Bida trong quán:</div>
                    <div style="max-height: 280px; overflow-y: auto; background: rgba(0,0,0,0.25); border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                        <table style="width: 100%; border-collapse: collapse; font-size: 12px; text-align: left;">
                            <thead>
                                <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); color: #a5b4fc; font-weight: 700;">
                                    <th style="padding: 10px 8px;">TÊN BÀN</th>
                                    <th style="padding: 10px 8px;">LOẠI BÀN</th>
                                    <th style="padding: 10px 8px;">TIÊU CHUẨN</th>
                                    <th style="padding: 10px 8px;">CAMERA</th>
                                    <th style="padding: 10px 8px; text-align: right;">GIÁ/GIỜ (VNĐ)</th>
                                    <th style="padding: 10px 8px; text-align: center;">HÀNH ĐỘNG</th>
                                </tr>
                            </thead>
                            <tbody id="inventory-tables-body">
                                <!-- Tables listed here -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
                <button onclick="closeInventoryModal()" style="padding: 10px 24px; border-radius: 8px; border: none; background: #4b5563; color: white; font-weight: bold; cursor: pointer; transition: background 0.2s;" onmouseover="this.style.background='#374151'" onmouseout="this.style.background='#4b5563'">Đóng</button>
            </div>
        </div>
    </div>

    <!-- BILL INVOICE MODAL -->
    <div class="bill-modal-overlay" id="bill-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); z-index: 1000; align-items: center; justify-content: center;">
        <div class="card" style="width: 90%; max-width: 480px; background: #1e1b4b; border: 1px solid rgba(255,255,255,0.15); display: flex; flex-direction: column; gap: 16px; padding: 28px;">
            <div style="font-size: 18px; font-weight: 800; color: #fbbf24; border-bottom: 2px dashed rgba(255,255,255,0.15); padding-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span>🧾 HÓA ĐƠN THANH TOÁN</span>
                    <span id="bill-table-name" style="font-size: 13px; background: rgba(99,102,241,0.3); color: #a5b4fc; padding: 3px 10px; border-radius: 6px; font-weight:700;">Bàn 1</span>
                </div>
                <span style="cursor: pointer; color: #9ca3af; font-size: 20px; font-weight: bold; padding: 4px; transition: color 0.2s;" onclick="closeBillModal()" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'">✕</span>
            </div>
            
            <div style="font-size: 13px; color: #d1d5db; display: flex; flex-direction: column; gap: 6px;">
                <div style="display: flex; justify-content: space-between;"><span>Giờ vào:</span> <b id="bill-start-time">--:--</b></div>
                <div id="bill-end-time-row" style="display: flex; justify-content: space-between;"><span>Giờ ra:</span> <b id="bill-end-time">--:--</b></div>
                <div style="display: flex; justify-content: space-between;"><span>Tổng thời gian chơi:</span> <b id="bill-duration">0 phút</b></div>
                <div style="display: flex; justify-content: space-between; color: #86efac; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">
                    <span>Tiền giờ chơi:</span> <b id="bill-play-fee" style="font-variant-numeric: tabular-nums;">0 VNĐ</b>
                </div>
            </div>
            
            <div style="font-size: 13px; color: #d1d5db;">
                <div style="font-weight: 700; color: #a5b4fc; margin-bottom: 8px;">Chi tiết món gọi (nước ngọt, khô mực...):</div>
                <div style="max-height: 140px; overflow-y: auto; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.04);">
                    <table style="width: 100%; border-collapse: collapse; font-size: 12px; text-align: left;">
                        <thead>
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); color: #fbbf24; font-weight: 700;">
                                <th style="padding: 4px 0; font-size: 11px;">TÊN MÓN</th>
                                <th style="padding: 4px 8px; text-align: center; font-size: 11px;">SL</th>
                                <th style="padding: 4px 8px; text-align: right; font-size: 11px;">ĐƠN GIÁ</th>
                                <th style="padding: 4px 0; text-align: right; font-size: 11px;">TỔNG TIỀN</th>
                            </tr>
                        </thead>
                        <tbody id="bill-items-body">
                            <!-- Items listed here -->
                        </tbody>
                    </table>
                </div>
                <div style="display: flex; justify-content: space-between; color: #86efac; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 8px; margin-top: 8px;">
                    <span>Tổng tiền dịch vụ:</span> <b id="bill-service-fee" style="font-variant-numeric: tabular-nums;">0 VNĐ</b>
                </div>
            </div>
            
            <div style="font-size: 20px; font-weight: 800; display: flex; justify-content: space-between; border-top: 2px dashed rgba(255,255,255,0.15); padding-top: 14px; color: #22c55e;">
                <span>TỔNG THANH TOÁN:</span>
                <span id="bill-total-amount" style="font-variant-numeric: tabular-nums;">0 VNĐ</span>
            </div>
            
            <div style="display: flex; gap: 10px; width: 100%;">
                <button class="btn btn-confirm" style="flex: 1; justify-content: center; font-size: 14px; padding: 12px; background: linear-gradient(135deg, #3b82f6, #2563eb);" onclick="printBill()">🖨️ In Bill Tạm Tính</button>
                <button id="bill-confirm-btn" class="btn btn-confirm" style="flex: 1; justify-content: center; font-size: 14px; padding: 12px;" onclick="closeBillModal()">✔️ Xác nhận & Thu tiền</button>
            </div>
        </div>
    </div>

    <!-- POS MODAL -->
    <div id="pos-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 2000; align-items: center; justify-content: center; backdrop-filter: blur(4px);">
        <div style="background: #1e1b4b; width: 95%; max-width: 1200px; height: 90vh; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">
            <!-- Header -->
            <div style="padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02);">
                <div style="font-size: 20px; font-weight: bold; color: #34d399;" id="pos-title">🛒 Thu Ngân Gọi Món - Bàn X</div>
                <button onclick="closePosModal()" style="background: transparent; border: none; color: #9ca3af; font-size: 28px; cursor: pointer;">&times;</button>
            </div>
            
            <!-- Body -->
            <div style="display: flex; flex: 1; overflow: hidden;">
                <!-- Left: Menu (70%) -->
                <div style="flex: 7; display: flex; flex-direction: column; border-right: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.2);">
                    <div id="pos-categories" style="display: flex; gap: 8px; padding: 16px; overflow-x: auto; border-bottom: 1px solid rgba(255,255,255,0.05); scrollbar-width: none;">
                        <!-- Categories injected here -->
                    </div>
                    <div id="pos-products" style="flex: 1; padding: 16px; overflow-y: auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; align-content: start;">
                        <!-- Products injected here -->
                    </div>
                </div>
                
                <!-- Right: Cart (30%) -->
                <div style="flex: 3; display: flex; flex-direction: column; background: rgba(255,255,255,0.02);">
                    <div style="padding: 16px; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 16px; text-align: center; color: white;">GIỎ HÀNG</div>
                    <div id="pos-cart-items" style="flex: 1; padding: 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px;">
                        <!-- Cart items injected here -->
                    </div>
                    <div style="padding: 16px; border-top: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.3);">
                        <div style="display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; margin-bottom: 16px; color: white;">
                            <span>Tổng cộng:</span>
                            <span id="pos-total-price" style="color: #34d399;">0đ</span>
                        </div>
                        <button id="pos-submit-btn" onclick="submitPosOrder()" style="width: 100%; padding: 14px; background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer;">Xác nhận thêm vào Bàn</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- QR CODE MODAL -->
    <div class="bill-modal-overlay" id="qr-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); z-index: 1000; align-items: center; justify-content: center;">
        <div class="card" style="width: 90%; max-width: 380px; background: #1e1b4b; border: 1px solid rgba(255,255,255,0.15); display: flex; flex-direction: column; gap: 16px; padding: 28px; text-align: center; align-items: center;">
            <div style="font-size: 18px; font-weight: 800; color: #fbbf24; width: 100%; border-bottom: 2px dashed rgba(255,255,255,0.15); padding-bottom: 12px;" id="qr-modal-title">
                📷 MÃ QR GỌI MÓN - BÀN X
            </div>
            <div style="background: white; padding: 12px; border-radius: 12px; display: inline-block; margin: 10px 0;">
                <img id="qr-modal-image" src="" alt="QR Code" style="width: 200px; height: 200px; display: block;">
            </div>
            <p style="font-size: 13px; color: #9ca3af; line-height: 1.5; margin: 0;">
                Khách hàng quét mã này bằng điện thoại để hiển thị thực đơn gọi đồ uống, dịch vụ.
            </p>
            <div style="font-size: 11px; color: #818cf8; word-break: break-all;" id="qr-modal-link">
                Link: http://...
            </div>
            <button class="btn btn-confirm" style="width: 100%; justify-content: center; font-size: 14px; padding: 12px; margin-top: 10px;" onclick="closeQRModal()">Đóng</button>
        </div>
    </div>

    <!-- REJECT TRANSFER CUSTOM MODAL (IMAGE 2 DESIGN) -->
    <div class="custom-confirm-overlay" id="reject-transfer-modal">
        <div class="custom-confirm-card">
            <div class="custom-modal-icon">!</div>
            <div class="custom-modal-title">Từ chối yêu cầu đổi bàn?</div>
            <div class="custom-modal-sub" id="reject-modal-sub">Vui lòng chọn lý do từ chối yêu cầu đổi bàn của khách</div>
            
            <div class="custom-modal-options">
                <label class="custom-modal-radio">
                    <input type="radio" name="reject_reason" value="1" checked onchange="toggleRejectOtherInput()">
                    <span>1 - Tạm thời hết bàn trống</span>
                </label>
                <label class="custom-modal-radio">
                    <input type="radio" name="reject_reason" value="2" onchange="toggleRejectOtherInput()">
                    <span>2 - Bàn đang bảo trì / hỏng</span>
                </label>
                <label class="custom-modal-radio">
                    <input type="radio" name="reject_reason" value="3" onchange="toggleRejectOtherInput()">
                    <span>3 - Lý do khác...</span>
                </label>
                <input type="text" id="reject-other-input" class="custom-modal-input" placeholder="Nhập lý do cụ thể..." style="display: none;">
            </div>

            <div class="custom-modal-btns">
                <button class="btn-custom-confirm" onclick="confirmRejectTransfer()">Đồng ý</button>
                <button class="btn-custom-cancel" onclick="closeRejectTransferModal()">Hủy</button>
            </div>
        </div>
    </div>

    <!-- APPROVE TRANSFER CUSTOM MODAL -->
    <div class="custom-confirm-overlay" id="approve-transfer-modal">
        <div class="custom-confirm-card">
            <div class="custom-modal-icon info">🔄</div>
            <div class="custom-modal-title">Chuyển sang bàn nào?</div>
            <div class="custom-modal-sub" id="approve-modal-sub">Chọn bàn đích để chuyển phiên chơi cho khách</div>
            
            <div style="margin-bottom: 20px; text-align: left;">
                <label style="font-size: 13px; color: #4b5563; font-weight: 700; display: block; margin-bottom: 6px;">Danh sách bàn trống khả dụng:</label>
                <select id="transfer-target-select" class="custom-modal-select"></select>
            </div>

            <div class="custom-modal-btns">
                <button class="btn-custom-confirm" onclick="confirmTransferTable()">Đồng ý</button>
                <button class="btn-custom-cancel" onclick="closeTransferModal()">Hủy</button>
            </div>
        </div>
    </div>

    <script>
        window.onerror = function(msg, url, lineNo, columnNo, error) {
            var bannerText = document.getElementById("banner-text");
            var statusBanner = document.getElementById("status-banner");
            if(bannerText) {
                statusBanner.className = "status-banner status-error";
                bannerText.textContent = "Lỗi JS: " + msg + " (Dòng " + lineNo + ")";
            }
            return false;
        };
        
        var eventsDiv = document.getElementById("events");
        var emptyState = document.getElementById("empty-state");
        var statusDot = document.getElementById("status-dot");
        var statusLabel = document.getElementById("status-label");
        var statusBanner = document.getElementById("status-banner");
        var bannerIcon = document.getElementById("banner-icon");
        var bannerText = document.getElementById("banner-text");
        var clockEl = document.getElementById("clock");
        var eventCountEl = document.getElementById("event-count");
        var soundBtn = document.getElementById("sound-btn");
        var tablesGrid = document.getElementById("tables-grid");
        
        var currentCamTableId = 1;

        var pollCount = 0;
        var eventCount = 0;
        var lastImage = "";
        var soundEnabled = true;
        var audioCtx = null;
        
        var tablesLocalData = [];
        var currentTableFilter = "all"; // all, empty, playing
        var streamStates = {}; // key: tableId, value: true/false (stream status)

        function syncStreamStates(tables) {
            tables.forEach(function(t) {
                var container = document.getElementById("cam-container-" + t.id);
                var statusBadge = document.getElementById("cam-status-" + t.id);
                
                if (container && statusBadge) {
                    // 1. Phân biệt màu sắc viền và badge bàn trống / bàn hoạt động
                    if (t.current_status === "PLAYING") {
                        container.className = "live-stream-container active-table";
                        statusBadge.className = "stream-status-badge status-active-playing";
                        statusBadge.textContent = "ĐANG CHƠI";
                        
                        // Tự động bật stream khi bàn chuyển trạng thái từ trống sang có khách chơi
                        if (streamStates[t.id] === undefined) {
                            streamStates[t.id] = true;
                        }
                    } else {
                        container.className = "live-stream-container empty-table";
                        statusBadge.className = "stream-status-badge status-empty-waiting";
                        statusBadge.textContent = "BÀN TRỐNG";
                        
                        // Bàn trống thì mặc định tắt stream để tiết kiệm băng thông mạng & CPU
                        if (streamStates[t.id] === undefined) {
                            streamStates[t.id] = false;
                        }
                    }
                    
                    // 2. Đồng bộ trạng thái stream (Hiển thị overlay đen và đổi nút)
                    var overlay = document.getElementById("cam-overlay-" + t.id);
                    var hoverOverlay = document.getElementById("cam-hover-" + t.id);
                    
                    if (streamStates[t.id]) {
                        if (overlay) overlay.className = "stream-overlay hidden";
                        if (hoverOverlay) hoverOverlay.style.display = "flex";
                    } else {
                        if (overlay) overlay.className = "stream-overlay";
                        if (hoverOverlay) hoverOverlay.style.display = "none";
                        
                        // Xóa thuộc tính src của thẻ img để trình duyệt ngừng call API live
                        var liveImg = document.getElementById("live-cam-" + t.id);
                        if (liveImg && !liveImg.src.includes("photo-1544197150-b99a580bb7a8")) {
                            liveImg.removeAttribute("src");
                        }
                    }
                }
            });
        }

        function toggleCamStream(tableId) {
            // Ngăn sự kiện click bọt (stopPropagation) nếu cần
            if (window.event) window.event.stopPropagation();
            
            streamStates[tableId] = !streamStates[tableId];
            syncStreamStates(tablesLocalData);
        }

        function toggleSidebar() {
            var sidebar = document.getElementById("sidebar");
            if (sidebar) {
                sidebar.classList.toggle("collapsed");
            }
        }

        function toggleDrawer(isOpen) {
            var drawer = document.getElementById("highlight-drawer");
            var overlay = document.getElementById("drawer-overlay");
            if (drawer && overlay) {
                if (isOpen) {
                    drawer.classList.add("open");
                    overlay.classList.add("open");
                    overlay.style.display = "block";
                } else {
                    drawer.classList.remove("open");
                    overlay.classList.remove("open");
                    setTimeout(function() {
                        if (!drawer.classList.contains("open")) {
                            overlay.style.display = "none";
                        }
                    }, 300);
                }
            }
        }

        function setTableFilter(filterType, element) {
            currentTableFilter = filterType;
            
            // Xoa active class khoi tat ca link
            var links = document.querySelectorAll(".sidebar-link");
            links.forEach(function(link) {
                link.classList.remove("active");
            });
            
            // Them active class cho link vua bam
            if (element) {
                element.classList.add("active");
            }
            
            // Render lai grid voi filter moi
            renderTablesGrid(tablesLocalData);
        }

        // === CLOCK ===
        function updateClock() {
            var now = new Date();
            var h = now.getHours();
            var m = now.getMinutes();
            var s = now.getSeconds();
            clockEl.textContent = (h < 10 ? "0" + h : h) + ":" + (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
        }
        setInterval(updateClock, 1000);
        updateClock();

        // === LIVE CAM REFRESH ===
        // Chỉ refresh ảnh của các camera đang ở trạng thái Bật Stream (streamStates[id] = true)
        function refreshCam(id) {
            if (!streamStates[id]) {
                setTimeout(function() { refreshCam(id); }, 1500);
                return;
            }
            var liveImg = document.getElementById("live-cam-" + id);
            if (!liveImg) {
                setTimeout(function() { refreshCam(id); }, 1500);
                return;
            }
            var newImg = new Image();
            newImg.onload = function() {
                liveImg.src = newImg.src;
                setTimeout(function() { refreshCam(id); }, 1500);
            };
            newImg.onerror = function() {
                setTimeout(function() { refreshCam(id); }, 1500);
            };
            newImg.src = "/api/live/" + id + "?t=" + Date.now();
        }
        for (var camId = 1; camId <= 4; camId++) {
            refreshCam(camId);
        }

        // === SOUND ===
        function toggleSound() {
            soundEnabled = !soundEnabled;
            soundBtn.className = soundEnabled ? "sound-toggle active" : "sound-toggle";
            document.getElementById("sound-icon").innerHTML = soundEnabled ? "&#128264;" : "&#128263;";
        }
        soundBtn.className = "sound-toggle active";

        function playAlert() {
            if (!soundEnabled) return;
            try {
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                var o1 = audioCtx.createOscillator();
                var g1 = audioCtx.createGain();
                o1.connect(g1); g1.connect(audioCtx.destination);
                o1.type = "sine"; o1.frequency.value = 880;
                g1.gain.setValueAtTime(0.3, audioCtx.currentTime);
                g1.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
                o1.start(audioCtx.currentTime); o1.stop(audioCtx.currentTime + 0.5);
                
                var o2 = audioCtx.createOscillator();
                var g2 = audioCtx.createGain();
                o2.connect(g2); g2.connect(audioCtx.destination);
                o2.type = "sine"; o2.frequency.value = 1100;
                g2.gain.setValueAtTime(0.3, audioCtx.currentTime + 0.15);
                g2.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.65);
                o2.start(audioCtx.currentTime + 0.15); o2.stop(audioCtx.currentTime + 0.65);
            } catch(e) {}
        }
        
        function playOrderAlert() {
            if (!soundEnabled) return;
            try {
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                var freqs = [523.25, 659.25, 783.99, 1046.50];
                var startTime = audioCtx.currentTime;
                freqs.forEach(function(f, i) {
                    var o = audioCtx.createOscillator();
                    var g = audioCtx.createGain();
                    o.connect(g); g.connect(audioCtx.destination);
                    o.type = "sine"; 
                    o.frequency.value = f;
                    g.gain.setValueAtTime(0.4, startTime + i * 0.15);
                    g.gain.exponentialRampToValueAtTime(0.001, startTime + i * 0.15 + 0.3);
                    o.start(startTime + i * 0.15); 
                    o.stop(startTime + i * 0.15 + 0.3);
                });
            } catch(e) {}
        }

        // === HISTORY MODAL LOGIC ===
        function openHistoryModal() {
            document.getElementById('history-modal').style.display = 'flex';
            loadHistory();
        }

        function closeHistoryModal() {
            document.getElementById('history-modal').style.display = 'none';
        }

        function loadHistory() {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/history', true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var history = JSON.parse(xhr.responseText);
                    var tbody = document.getElementById('history-items-body');
                    tbody.innerHTML = '';
                    history.forEach(function(h) {
                        var canDeleteAttr = h.can_delete ? "data-candelete='true'" : "data-candelete='false' disabled";
                        var chkHtml = '<input type="checkbox" class="chk-history" value="' + h.id + '" ' + canDeleteAttr + ' onchange="updateHistoryDeleteBtn()">';
                        
                        var tr = document.createElement('tr');
                        tr.style.borderBottom = "1px solid rgba(255,255,255,0.06)";
                        tr.innerHTML = `
                            <td style="padding: 10px 8px; text-align: center;">${chkHtml}</td>
                            <td style="padding: 10px 8px;">${h.table_name}</td>
                            <td style="padding: 10px 8px;">${new Date(h.start_time).toLocaleString('vi-VN')}</td>
                            <td style="padding: 10px 8px;">${new Date(h.end_time).toLocaleString('vi-VN')}</td>
                            <td style="padding: 10px 8px; text-align: right;">${h.total_minutes} phút</td>
                            <td style="padding: 10px 8px; text-align: right; color: #86efac; font-weight: bold;">${h.total_bill.toLocaleString('vi-VN')} đ</td>
                            <td style="padding: 10px 8px; text-align: center;">
                                <button onclick="toggleHistoryDetail(${h.id})" style="padding: 4px 8px; background: rgba(99,102,241,0.2); border: 1px solid rgba(99,102,241,0.4); color: #a5b4fc; border-radius: 4px; cursor: pointer;">Chi tiết ⬇</button>
                            </td>
                        `;
                        if (!h.can_delete) {
                            tr.style.opacity = "0.6";
                        }
                        
                        var itemsHtml = h.items.map(function(item) {
                            return `<tr><td style="padding: 4px 8px;">${item.item_name}</td><td style="padding: 4px 8px; text-align: center;">${item.quantity}</td><td style="padding: 4px 8px; text-align: right;">${item.total_price.toLocaleString('vi-VN')} đ</td></tr>`;
                        }).join("");
                        
                        var detailTr = document.createElement('tr');
                        detailTr.id = 'history-detail-' + h.id;
                        detailTr.style.display = 'none';
                        detailTr.innerHTML = `
                            <td colspan="7" style="padding: 10px 24px; background: rgba(0,0,0,0.3); border-bottom: 1px solid rgba(255,255,255,0.06);">
                                <div style="font-size: 11px; color: #9ca3af; margin-bottom: 6px;">Tiền giờ: <b style="color: white;">${h.play_fee.toLocaleString('vi-VN')} đ</b></div>
                                <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                                    <tr style="color: #fbbf24; border-bottom: 1px dashed rgba(255,255,255,0.1);">
                                        <th style="padding: 4px 8px; text-align: left;">Món ăn / Dịch vụ</th>
                                        <th style="padding: 4px 8px;">SL</th>
                                        <th style="padding: 4px 8px; text-align: right;">Thành tiền</th>
                                    </tr>
                                    ${itemsHtml || '<tr><td colspan="3" style="padding: 4px 8px; text-align: center; color: #6b7280;">Không gọi thêm món</td></tr>'}
                                </table>
                            </td>
                        `;
                        
                        tbody.appendChild(tr);
                        tbody.appendChild(detailTr);
                    });
                    updateHistoryDeleteBtn();
                }
            };
            xhr.send();
        }

        function toggleHistoryDetail(id) {
            var tr = document.getElementById('history-detail-' + id);
            if (tr) {
                tr.style.display = tr.style.display === 'none' ? 'table-row' : 'none';
            }
        }

        function toggleAllHistory(source) {
            var checkboxes = document.querySelectorAll('.chk-history:not([disabled])');
            for (var i = 0; i < checkboxes.length; i++) {
                checkboxes[i].checked = source.checked;
            }
            updateHistoryDeleteBtn();
        }

        function updateHistoryDeleteBtn() {
            var checkboxes = document.querySelectorAll('.chk-history:checked');
            var btn = document.getElementById('btn-delete-history');
            if (checkboxes.length > 0) {
                btn.disabled = false;
                btn.style.opacity = '1';
                btn.textContent = '🗑️ Xóa đã chọn (' + checkboxes.length + ')';
            } else {
                btn.disabled = true;
                btn.style.opacity = '0.5';
                btn.textContent = '🗑️ Xóa đã chọn';
            }
        }

        function deleteSelectedHistory() {
            var checkboxes = document.querySelectorAll('.chk-history:checked');
            var ids = Array.from(checkboxes).map(function(c) { return parseInt(c.value); });
            if (ids.length === 0) return;
            
            if (!confirm('Bạn có chắc chắn muốn xóa ' + ids.length + ' phiên chơi này? Hành động này không thể hoàn tác.')) return;
            
            var xhr = new XMLHttpRequest();
            xhr.open('DELETE', '/api/history', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onload = function() {
                if (xhr.status === 200) {
                    alert('Đã xóa thành công!');
                    document.getElementById('chk-all-history').checked = false;
                    loadHistory();
                } else {
                    alert('Lỗi khi xóa: ' + xhr.responseText);
                }
            };
            xhr.send(JSON.stringify({ session_ids: ids }));
        }

        // === LOAD TABLES DATA ===
        function loadTables() {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/tables?_" + Date.now(), true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var tables = JSON.parse(xhr.responseText);
                    tablesLocalData = tables;
                    renderTablesGrid(tables);
                    syncStreamStates(tables); // Cập nhật trạng thái bật/tắt camera
                }
                setTimeout(loadTables, 3000);
            };
            xhr.onerror = function() {
                setTimeout(loadTables, 3000);
            };
            xhr.send();
        }

        // Luu tru trang thai form dang mo va cac gia tri input de khong bi reset khi loadTables
        var openForms = {}; 
        var formSelectedItems = {};
        var formQuantities = {};

        function renderTablesGrid(tables) {
            tablesGrid.innerHTML = "";
            
            // Bo loc trang thai ban choi
            var filteredTables = tables.filter(function(t) {
                if (currentTableFilter === "empty") {
                    return t.current_status !== "PLAYING";
                } else if (currentTableFilter === "playing") {
                    return t.current_status === "PLAYING";
                }
                return true; // "all"
            });
            
            if (filteredTables.length === 0) {
                tablesGrid.innerHTML = "<div style='grid-column: span 2; text-align: center; padding: 40px; color: #8b949e; font-size: 13px; font-weight: 500;'>Không có bàn nào phù hợp với bộ lọc hiện tại.</div>";
                return;
            }
            
            filteredTables.forEach(function(t) {
                var card = document.createElement("div");
                card.className = t.current_status === "PLAYING" ? "table-card playing" : "table-card";
                
                // Header card
                var header = document.createElement("div");
                header.className = "table-card-header";
                
                var nameSpan = document.createElement("span");
                nameSpan.className = "table-name";
                nameSpan.innerHTML = t.name;
                
                var badgesDiv = document.createElement("div");
                badgesDiv.className = "table-badges";
                
                var tierBadge = document.createElement("span");
                tierBadge.className = t.table_tier === "VIP" ? "badge-vip" : "badge-std";
                tierBadge.textContent = t.table_tier === "VIP" ? "VIP" : "Thường";
                
                var typeBadge = document.createElement("span");
                typeBadge.className = "badge-type";
                typeBadge.textContent = t.table_type === "LIP" ? "Líp" : "Phăng 3C";
                
                badgesDiv.appendChild(tierBadge);
                badgesDiv.appendChild(typeBadge);
                header.appendChild(nameSpan);
                header.appendChild(badgesDiv);
                card.appendChild(header);
                
                // Status label
                var statusDiv = document.createElement("div");
                statusDiv.style.fontSize = "13px";
                statusDiv.innerHTML = "Trạng thái: " + 
                    (t.current_status === "PLAYING" 
                        ? "<span class='table-status-label status-playing'>● Đang chơi</span>" 
                        : "<span class='table-status-label status-empty'>● Bàn trống</span>");
                card.appendChild(statusDiv);
                
                // Table details (Ghi bill & Thoi gian choi)
                var details = document.createElement("div");
                details.className = "table-details";
                
                if (t.current_status === "PLAYING" && t.active_session) {
                    details.style.cursor = "pointer";
                    details.title = "Nhấn để xem chi tiết hóa đơn";
                    details.addEventListener("click", function() { viewActiveBill(t.id); });
                    
                    var startTime = new Date(t.active_session.start_time);
                    var hour = startTime.getHours();
                    var min = startTime.getMinutes();
                    var timeStr = (hour < 10 ? "0" + hour : hour) + ":" + (min < 10 ? "0" + min : min);
                    
                    // Tinh nhanh tien va gio theo realtime
                    var diffMs = new Date() - startTime;
                    var diffSecs = Math.max(0, Math.floor(diffMs / 1000));
                    var diffMins = Math.floor(diffSecs / 60);
                    var diffHours = Math.floor(diffMins / 60);
                    var minsLeft = diffMins % 60;
                    
                    var durationText = diffHours > 0 ? diffHours + "h " + minsLeft + "m" : diffMins + "m";
                    
                    // Tinh tien gio
                    var playFee = Math.ceil((diffMins / 60) * t.price_per_hour);
                    
                    // Tinh tien dich vu mon an nuoc uong
                    var serviceTotal = 0;
                    var itemsText = "";
                    if (t.active_session.order_items && t.active_session.order_items.length > 0) {
                        t.active_session.order_items.forEach(function(item) {
                            serviceTotal += item.total_price;
                        });
                        itemsText = "<div style='color: #818cf8; margin-top: 4px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 4px;'>Đồ gọi thêm: " + 
                            t.active_session.order_items.map(function(i){return i.item_name + " x" + i.quantity;}).join(", ") + "</div>";
                    }
                    
                    var totalBill = playFee + serviceTotal;
                    
                    details.innerHTML = 
                        "<div>Vào lúc: <b>" + timeStr + "</b></div>" +
                        "<div>Đã chơi: <b style='color: #fbbf24;'>" + durationText + "</b></div>" +
                        "<div>Tiền giờ: <b>" + playFee.toLocaleString("vi-VN") + " đ</b></div>" +
                        "<div>Tiền dịch vụ: <b>" + serviceTotal.toLocaleString("vi-VN") + " đ</b></div>" +
                        "<div style='border-top: 1px solid rgba(255,255,255,0.1); padding-top:4px; margin-top:2px; color: #86efac; font-weight:700;'>TỔNG BILL: " + totalBill.toLocaleString("vi-VN") + " đ</div>" +
                        itemsText;
                } else {
                    details.innerHTML = 
                        "<div>Đơn giá: <b>" + t.price_per_hour.toLocaleString("vi-VN") + " VNĐ/h</b></div>" +
                        "<div style='color: #6b7280;'>Sẵn sàng đón khách mới</div>";
                }
                card.appendChild(details);
                
                // Button Actions
                var btnGroup = document.createElement("div");
                btnGroup.className = "order-btn-group";
                
                if (t.current_status === "PLAYING") {
                    
                    // Nut Thanh toan
                    var btnStop = document.createElement("button");
                    btnStop.className = "btn btn-confirm btn-small";
                    btnStop.innerHTML = "🔴 Thanh toán";
                    btnStop.addEventListener("click", function() {
                        checkoutSession(t.id);
                    });
                    btnGroup.appendChild(btnStop);
                    
                    // Nut In Bill Tạm Tính
                    var btnPrintTemp = document.createElement("button");
                    btnPrintTemp.className = "btn btn-dismiss btn-small";
                    btnPrintTemp.style.cssText = "background: rgba(99, 102, 241, 0.15); border-color: rgba(99, 102, 241, 0.3); color: #a5b4fc;";
                    btnPrintTemp.innerHTML = "🖨️ In Tạm Tính";
                    btnPrintTemp.addEventListener("click", function(e) {
                        e.stopPropagation();
                        viewActiveBill(t.id, true);
                    });
                    btnGroup.appendChild(btnPrintTemp);
                    
                    // Nut Chuyen ban
                    var btnTransfer = document.createElement("button");
                    btnTransfer.className = "btn btn-dismiss btn-small";
                    btnTransfer.style.cssText = "background: rgba(14, 165, 233, 0.15); border-color: rgba(14, 165, 233, 0.3); color: #7dd3fc;";
                    btnTransfer.innerHTML = "🔄 Chuyển bàn";
                    btnTransfer.addEventListener("click", function(e) {
                        e.stopPropagation();
                        showTransferModal(t.id);
                    });
                    btnGroup.appendChild(btnTransfer);
                } else {
                    // Nut Bat dau choi
                    var btnStart = document.createElement("button");
                    btnStart.className = "btn btn-confirm btn-small";
                    btnStart.style.background = "linear-gradient(135deg, #6366f1, #4f46e5)";
                    btnStart.innerHTML = "🟢 Bắt đầu chơi";
                    btnStart.addEventListener("click", function() {
                        startSession(t.id);
                    });
                    btnGroup.appendChild(btnStart);
                }
                
                // Nut ma QR
                var btnQR = document.createElement("button");
                btnQR.className = "btn btn-dismiss btn-small";
                btnQR.style.cssText = "background: rgba(245, 158, 11, 0.12); border-color: rgba(245, 158, 11, 0.25); color: #fbbf24;";
                btnQR.innerHTML = "📷 Mã QR";
                btnQR.addEventListener("click", function() {
                    showTableQRModal(t.id, t.name, t.qr_token);
                });
                btnGroup.appendChild(btnQR);
                
                card.appendChild(btnGroup);
                
                // Nút Mở Giao Diện POS (chỉ hiện khi bàn đang chơi)
                if (t.current_status === "PLAYING") {
                    var btnPos = document.createElement("button");
                    btnPos.className = "btn btn-primary btn-small";
                    btnPos.style.cssText = "background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3); color: #34d399; width: 100%; margin-top: 8px; font-weight: bold;";
                    btnPos.innerHTML = "🛒 Thu ngân gọi món";
                    btnPos.addEventListener("click", function() {
                        openPosModal(t.id, t.name);
                    });
                    card.appendChild(btnPos);
                }
                
                tablesGrid.appendChild(card);
            });
        }
        


        function requestSelectedClip() {
            var tableSelect = document.getElementById("highlight-table-select");
            if (tableSelect) {
                requestClip(parseInt(tableSelect.value));
            }
        }
        function requestSelectedPastClip() {
            var tableSelect = document.getElementById("highlight-table-select");
            if (tableSelect) {
                requestPastClip(parseInt(tableSelect.value));
            }
        }

        // === START SESSION API ===
        function startSession(tableId) {
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/session/start/" + tableId, true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    loadTables();
                } else {
                    var errMsg = "Không thể bắt đầu phiên chơi!";
                    try {
                        var res = JSON.parse(xhr.responseText);
                        if (res && res.message) errMsg = res.message;
                    } catch(e) {}
                    alert(errMsg);
                }
            };
            xhr.send();
        }



        // === TRANSFER TABLE ===
        var currentTransferFromId = null;
        var currentRejectTableId = null;

        function toggleRejectOtherInput() {
            var radios = document.getElementsByName("reject_reason");
            var selectedVal = "1";
            for (var i = 0; i < radios.length; i++) {
                if (radios[i].checked) selectedVal = radios[i].value;
            }
            var otherInput = document.getElementById("reject-other-input");
            if (selectedVal === "3") {
                otherInput.style.display = "block";
                otherInput.focus();
            } else {
                otherInput.style.display = "none";
            }
        }

        function showRejectTransferModal(tableId) {
            currentRejectTableId = tableId;
            var fromTable = tablesLocalData.find(function(t) { return t.id === tableId; });
            var tableName = fromTable ? fromTable.name : ("Bàn " + tableId);
            
            var subEl = document.getElementById("reject-modal-sub");
            if (subEl) subEl.textContent = "Từ chối yêu cầu đổi bàn của " + tableName;
            var radios = document.getElementsByName("reject_reason");
            if (radios && radios.length > 0) radios[0].checked = true;
            var otherInput = document.getElementById("reject-other-input");
            if (otherInput) { otherInput.style.display = "none"; otherInput.value = ""; }
            var modalEl = document.getElementById("reject-transfer-modal");
            if (modalEl) modalEl.style.display = "flex";
        }

        function closeRejectTransferModal() {
            document.getElementById("reject-transfer-modal").style.display = "none";
            currentRejectTableId = null;
        }

        function confirmRejectTransfer() {
            if (!currentRejectTableId) return;
            var tableId = currentRejectTableId;
            
            var radios = document.getElementsByName("reject_reason");
            var selectedVal = "1";
            for (var i = 0; i < radios.length; i++) {
                if (radios[i].checked) selectedVal = radios[i].value;
            }
            
            var reason = "";
            if (selectedVal === "1") reason = "Hết bàn trống, mong quý khách thông cảm!";
            else if (selectedVal === "2") reason = "Bàn yêu cầu đang bảo trì, mong quý khách thông cảm!";
            else if (selectedVal === "3") {
                reason = document.getElementById("reject-other-input").value.trim();
                if (!reason) {
                    alert("Vui lòng nhập lý do từ chối cụ thể!");
                    return;
                }
            }
            
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/client-notify/" + tableId, true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onload = function() {
                alert("Đã gửi thông báo từ chối tới khách!");
                closeRejectTransferModal();
                loadTables();
            };
            xhr.send(JSON.stringify({
                message: "Yêu cầu đổi bàn đã bị từ chối. Lý do: " + reason,
                type: "error"
            }));
        }

        function showTransferModal(fromTableId, requestedType) {
            currentTransferFromId = fromTableId;
            var fromTable = tablesLocalData.find(function(t) { return t.id === fromTableId; });
            var fromName = fromTable ? fromTable.name : ("Bàn " + fromTableId);
            
            var emptyTables = tablesLocalData.filter(function(t) { return t.current_status === "EMPTY"; });
            
            var typeName = "";
            if (requestedType) {
                emptyTables = emptyTables.filter(function(t) { return t.table_type === requestedType; });
                if (requestedType === "LIP") typeName = "Líp";
                else if (requestedType === "3C") typeName = "3 Băng";
                else if (requestedType === "POOL") typeName = "Lỗ";
                
                if (emptyTables.length === 0) {
                    alert("Hiện tại không có bàn " + typeName + " nào trống để chuyển. Đã tự động báo cho khách!");
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/api/client-notify/" + fromTableId, true);
                    xhr.setRequestHeader("Content-Type", "application/json");
                    xhr.send(JSON.stringify({ message: "Tạm thời hết bàn " + typeName + ", mong quý khách thông cảm!", type: "error" }));
                    return;
                }
            } else {
                if (emptyTables.length === 0) {
                    alert("Hiện tại không có bàn nào trống để chuyển. Đã tự động báo cho khách!");
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/api/client-notify/" + fromTableId, true);
                    xhr.setRequestHeader("Content-Type", "application/json");
                    xhr.send(JSON.stringify({ message: "Tạm thời hết bàn, mong quý khách thông cảm!", type: "error" }));
                    return;
                }
            }
            
            var subEl = document.getElementById("approve-modal-sub");
            if (subEl) subEl.textContent = "Chuyển " + fromName + (typeName ? (" (Yêu cầu: bàn " + typeName + ")") : "") + " sang bàn trống:";
            
            var select = document.getElementById("transfer-target-select");
            select.innerHTML = "";
            emptyTables.forEach(function(t) {
                var opt = document.createElement("option");
                opt.value = t.id;
                var tTypeName = t.table_type === "LIP" ? "Líp" : (t.table_type === "3C" ? "3 Băng" : "Lỗ");
                opt.textContent = t.name + " (" + tTypeName + ")";
                select.appendChild(opt);
            });
            
            document.getElementById("approve-transfer-modal").style.display = "flex";
        }

        function closeTransferModal() {
            document.getElementById("approve-transfer-modal").style.display = "none";
            currentTransferFromId = null;
        }

        function confirmTransferTable() {
            if (!currentTransferFromId) return;
            var select = document.getElementById("transfer-target-select");
            var toTableId = parseInt(select.value);
            if (!toTableId) {
                alert("Vui lòng chọn bàn đích!");
                return;
            }
            transferTable(currentTransferFromId, toTableId);
            closeTransferModal();
        }
        
        function transferTable(fromTableId, toTableId) {
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/session/transfer/" + fromTableId + "/" + toTableId, true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    alert("Chuyển bàn thành công!");
                    loadTables();
                } else {
                    var res = JSON.parse(xhr.responseText || "{}");
                    alert("Lỗi chuyển bàn: " + (res.message || xhr.statusText));
                }
            };
            xhr.send();
        }

        function checkoutSession(tableId) {
            Swal.fire({
                title: 'Xác nhận thanh toán?',
                text: "Bạn có chắc chắn muốn tính tiền và thanh toán hóa đơn cho bàn này?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#10b981',
                cancelButtonColor: '#ef4444',
                confirmButtonText: 'Đồng ý',
                cancelButtonText: 'Hủy'
            }).then((result) => {
                if (result.isConfirmed) {
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/api/session/stop/" + tableId, true);
                    xhr.onload = function() {
                        if (xhr.status === 200) {
                            var bill = JSON.parse(xhr.responseText);
                            Swal.fire({
                                title: 'Thanh toán thành công!',
                                text: 'Bạn có muốn in hóa đơn (Bill) giấy cho khách không?',
                                icon: 'success',
                                showCancelButton: true,
                                confirmButtonColor: '#10b981',
                                cancelButtonColor: '#6b7280',
                                confirmButtonText: '🖨️ In Hóa Đơn',
                                cancelButtonText: 'Không in'
                            }).then((printResult) => {
                                if (printResult.isConfirmed) {
                                    currentBillToPrint = bill;
                                    printBill(); 
                                }
                                loadTables();
                            });
                        } else {
                            Swal.fire('Lỗi!', 'Không thể thanh toán!', 'error');
                        }
                    };
                    xhr.send();
                }
            });
        }

        // === VIEW ACTIVE BILL PREVIEW ===
        function viewActiveBill(tableId, silentPrint = false) {
            var t = tablesLocalData.find(function(item) { return item.id === tableId; });
            if (!t || t.current_status !== "PLAYING" || !t.active_session) return;
            
            var startTime = new Date(t.active_session.start_time);
            var endTime = new Date();
            var diffMs = endTime - startTime;
            var diffMins = Math.max(0, Math.floor(diffMs / 60000));
            
            var playFee = Math.ceil((diffMins / 60) * t.price_per_hour);
            
            var itemsList = [];
            var serviceTotal = 0;
            if (t.active_session.order_items && t.active_session.order_items.length > 0) {
                t.active_session.order_items.forEach(function(item) {
                    serviceTotal += item.total_price;
                    itemsList.push({
                        item_name: item.item_name,
                        quantity: item.quantity,
                        price: item.price,
                        total_price: item.total_price
                    });
                });
            }
            
            var totalBill = playFee + serviceTotal;
            
            var tempBill = {
                table_name: t.name,
                start_time: t.active_session.start_time,
                end_time: endTime.toISOString(),
                total_minutes: diffMins,
                play_fee: playFee,
                items: itemsList,
                service_total: serviceTotal,
                total_bill: totalBill,
                is_preview: true
            };
            
            if (silentPrint) {
                currentBillToPrint = tempBill;
                printBill();
            } else {
                showBillInvoice(tempBill);
            }
        }

        // === SHOW BILL MODAL INVOICE ===
        function showBillInvoice(bill) {
            document.getElementById("bill-table-name").textContent = bill.table_name;
            
            var start = new Date(bill.start_time);
            var end = new Date(bill.end_time);
            
            document.getElementById("bill-start-time").textContent = start.toLocaleTimeString();
            document.getElementById("bill-end-time").textContent = end.toLocaleTimeString();
            
            var endTimeRow = document.getElementById("bill-end-time-row");
            if (endTimeRow) {
                endTimeRow.style.display = bill.is_preview ? "none" : "flex";
            }
            
            document.getElementById("bill-duration").textContent = bill.total_minutes + " phút";
            document.getElementById("bill-play-fee").textContent = Math.ceil(bill.play_fee).toLocaleString("vi-VN") + " VNĐ";
            
            var itemsBody = document.getElementById("bill-items-body");
            itemsBody.innerHTML = "";
            
            if (bill.items && bill.items.length > 0) {
                bill.items.forEach(function(item) {
                    var tr = document.createElement("tr");
                    tr.style.borderBottom = "1px solid rgba(255,255,255,0.04)";
                    tr.innerHTML = 
                        "<td style='padding: 6px 0; color: #e5e7eb;'>" + item.item_name + "</td>" +
                        "<td style='padding: 6px 8px; text-align: center; font-weight: 600; color: #fbbf24;'>" + item.quantity + "</td>" +
                        "<td style='padding: 6px 8px; text-align: right; font-variant-numeric: tabular-nums;'>" + Math.ceil(item.price).toLocaleString("vi-VN") + " đ</td>" +
                        "<td style='padding: 6px 0; text-align: right; font-weight: 700; color: white; font-variant-numeric: tabular-nums;'>" + Math.ceil(item.total_price).toLocaleString("vi-VN") + " đ</td>";
                    itemsBody.appendChild(tr);
                });
            } else {
                itemsBody.innerHTML = "<tr><td colspan='4' style='color:#6b7280; font-size:12px; padding: 12px 0; text-align: center;'>Không gọi đồ ăn nước uống</td></tr>";
            }
            
            document.getElementById("bill-service-fee").textContent = Math.ceil(bill.service_total).toLocaleString("vi-VN") + " VNĐ";
            document.getElementById("bill-total-amount").textContent = Math.ceil(bill.total_bill).toLocaleString("vi-VN") + " VNĐ";
            
            currentBillToPrint = bill;
            var modalConfirmBtn = document.getElementById("bill-confirm-btn");
            if (modalConfirmBtn) {
                if (bill.is_preview) {
                    modalConfirmBtn.innerHTML = "Đóng";
                    modalConfirmBtn.style.background = "#4b5563";
                } else {
                    modalConfirmBtn.innerHTML = "🖨️ In & Hoàn tất";
                    modalConfirmBtn.style.background = "linear-gradient(135deg, #10b981, #059669)";
                }
            }

            document.getElementById("bill-modal").style.display = "flex";
            playAlert();
        }

        var currentBillToPrint = null;
        function printBill() {
            if (!currentBillToPrint) return;
            var bill = currentBillToPrint;
            var itemsHtml = "";
            if (bill.items && bill.items.length > 0) {
                bill.items.forEach(function(item) {
                    itemsHtml += "<tr>" +
                        "<td>" + item.item_name + "</td>" +
                        "<td style='text-align:center;'>" + item.quantity + "</td>" +
                        "<td style='text-align:right;'>" + Math.ceil(item.price).toLocaleString("vi-VN") + "</td>" +
                        "<td style='text-align:right;'>" + Math.ceil(item.total_price).toLocaleString("vi-VN") + "</td>" +
                    "</tr>";
                });
            } else {
                itemsHtml = "<tr><td colspan='4' style='text-align:center;'>Không gọi dịch vụ</td></tr>";
            }
            
            var sTime = new Date(bill.start_time).toLocaleTimeString('vi-VN');
            var eTime = bill.is_preview ? "--:--" : new Date(bill.end_time).toLocaleTimeString('vi-VN');
            var printTime = new Date().toLocaleString('vi-VN');
            
            var html = "<html><head><title>In Hóa Đơn</title>" +
                "<style>" +
                "@media print { @page { margin: 0; } body { margin: 5mm; } }" +
                "body { font-family: 'Courier New', Courier, monospace; font-size: 13px; width: 300px; margin: 0 auto; color: black; background: white; }" +
                "h2 { text-align: center; margin: 0 0 5px 0; font-size: 20px; font-weight: bold; text-transform: uppercase; }" +
                ".header { text-align: center; margin-bottom: 15px; }" +
                ".header p { margin: 3px 0; font-size: 13px; }" +
                ".divider { border-bottom: 1px dashed #000; margin: 10px 0; }" +
                "table { width: 100%; border-collapse: collapse; margin-bottom: 10px; }" +
                "th { padding: 4px 0; border-bottom: 1px dashed #000; font-weight: bold; font-size: 12px; }" +
                "td { padding: 4px 0; font-size: 13px; border-bottom: 1px dashed #eee; }" +
                ".flex-row { display: flex; justify-content: space-between; margin-bottom: 4px; }" +
                ".total-row { display: flex; justify-content: space-between; font-weight: bold; font-size: 16px; margin-top: 5px; border-top: 1px solid #000; padding-top: 5px; }" +
                ".footer { text-align: center; margin-top: 15px; font-size: 12px; }" +
                ".footer p { margin: 3px 0; }" +
                "</style></head><body>" +
                "<div class='header'>" +
                "<h2>BIDA CLUB</h2>" +
                "<p>3xx Huỳnh Tấn Phát, Quận 7, HCM</p>" +
                "<p>SĐT: 0396 123 456</p>" +
                "<p>Mã hóa đơn: " + (bill.is_preview ? "Tạm Tính" : "HD-" + Date.now().toString().slice(-6)) + "</p>" +
                "</div>" +
                
                "<div class='divider'></div>" +
                "<div class='flex-row'><span>Bàn:</span> <strong>" + bill.table_name + "</strong></div>" +
                "<div class='flex-row'><span>Vào:</span> <span>" + sTime + "</span></div>" +
                "<div class='flex-row'><span>Ra:</span> <span>" + eTime + "</span></div>" +
                "<div class='flex-row'><span>Tổng thời gian:</span> <span>" + bill.total_minutes + " phút</span></div>" +
                "<div class='flex-row'><span>Đơn giá giờ:</span> <span>" + (bill.total_minutes > 0 ? Math.round((bill.play_fee / bill.total_minutes) * 60).toLocaleString("vi-VN") : "0") + " VNĐ</span></div>" +
                "<div class='divider'></div>" +
                
                "<table>" +
                "<tr><th style='text-align:left;'>Món</th><th style='text-align:center;'>SL</th><th style='text-align:right;'>Đ.Giá</th><th style='text-align:right;'>T.Tiền</th></tr>" +
                itemsHtml +
                "</table>" +
                
                "<div class='flex-row'><span>Tiền giờ chơi:</span> <span>" + Math.ceil(bill.play_fee).toLocaleString("vi-VN") + " VNĐ</span></div>" +
                "<div class='flex-row'><span>Tiền dịch vụ:</span> <span>" + Math.ceil(bill.service_total).toLocaleString("vi-VN") + " VNĐ</span></div>" +
                "<div class='total-row'><span>TỔNG CỘNG:</span> <span>" + Math.ceil(bill.total_bill).toLocaleString("vi-VN") + " VNĐ</span></div>" +
                
                "<div class='divider'></div>" +
                "<div class='flex-row' style='margin-bottom: 8px;'><span>Phương thức:</span> <span>Tiền mặt / CK</span></div>" +
                "<div class='flex-row'><span>SĐT Khách:</span> <span>...................</span></div>" +
                "<div class='flex-row'><span>Ghi chú:</span> <span>...................</span></div>" +
                "<div class='divider'></div>" +
                
                "<div style='text-align:center; margin-top: 10px;'>" +
                "<p style='font-size:12px; margin-bottom: 2px; font-weight:bold;'>Quét QR thanh toán</p>" +
                "<img src='https://img.vietqr.io/image/970436-0396123456-compact2.png?amount=" + Math.ceil(bill.total_bill) + "&accountName=BIDA CLUB' style='width: 120px; height: 120px;'/>" +
                "</div>" +
                
                "<div class='footer'>" +
                "<p><strong>WIFI: Bida club</strong></p>" +
                "<p>Pass: bidaclubxincamon</p>" +
                "<p>----------------------</p>" +
                "<p>Thu ngân: Admin</p>" +
                "<p>In lúc: " + printTime + "</p>" +
                "</div>" +
                "</div></body></html>";

            var iframe = document.getElementById("print-iframe");
            if (!iframe) {
                iframe = document.createElement("iframe");
                iframe.id = "print-iframe";
                iframe.style.position = "absolute";
                iframe.style.width = "0px";
                iframe.style.height = "0px";
                iframe.style.border = "none";
                document.body.appendChild(iframe);
            }
            var doc = iframe.contentWindow.document;
            doc.open();
            doc.write(html);
            doc.close();
            
            setTimeout(() => {
                iframe.contentWindow.focus();
                iframe.contentWindow.print();
            }, 500);
        }

        function closeBillModal() {
            document.getElementById("bill-modal").style.display = "none";
        }

        // === REPORT FUNCTIONS ===
        function openReportModal() {
            document.getElementById("report-modal").style.display = "flex";
            
            // Set default date to today
            var today = new Date().toISOString().split('T')[0];
            document.getElementById("report-start-date").value = today;
            document.getElementById("report-end-date").value = today;
        }

        function closeReportModal() {
            document.getElementById("report-modal").style.display = "none";
        }
        
        function downloadRevenueReport() {
            var startDate = document.getElementById("report-start-date").value;
            var endDate = document.getElementById("report-end-date").value;
            var url = "/api/reports/revenue";
            var params = [];
            if (startDate) params.push("start_date=" + startDate);
            if (endDate) params.push("end_date=" + endDate);
            
            if (params.length > 0) {
                url += "?" + params.join("&");
            }
            
            window.location.href = url;
            closeReportModal();
        }

        // === INVENTORY MANAGEMENT FUNCTIONS ===
        function openInventoryModal() {
            document.getElementById("inventory-modal").style.display = "flex";
            loadInventoryList();
        }

        function closeInventoryModal() {
            document.getElementById("inventory-modal").style.display = "none";
        }

        function toggleSelectAllProds(master) {
            var chks = document.querySelectorAll(".chk-prod");
            chks.forEach(function(c) {
                c.checked = master.checked;
            });
        }

        function loadInventoryList() {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/products", true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var prods = JSON.parse(xhr.responseText);
                    window.currentProdsList = prods;
                    var tbody = document.getElementById("inventory-items-body");
                    tbody.innerHTML = "";
                    
                    var master = document.getElementById("chk-all-prods");
                    if (master) master.checked = false;
                    
                    if (prods.length === 0) {
                        tbody.innerHTML = "<tr><td colspan='7' style='color:#6b7280; padding:12px; text-align:center;'>Chưa có sản phẩm nào</td></tr>";
                        return;
                    }
                    
                    prods.forEach(function(p) {
                        var tr = document.createElement("tr");
                        tr.style.borderBottom = "1px solid rgba(255,255,255,0.04)";
                        tr.innerHTML = 
                            "<td style='padding: 10px 8px; text-align:center;'><input type='checkbox' class='chk-prod' value='" + p.id + "'></td>" +
                            "<td style='padding: 10px 8px; font-weight:600; color:white;'>" + p.name + "</td>" +
                            "<td style='padding: 10px 8px;'><input list='cat-list' type='text' id='prod-cat-" + p.id + "' value='" + (p.category || '') + "' placeholder='Danh mục...' style='width:100px; height:28px; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:4px; color:#a5b4fc; padding:0 4px; font-size:11px; outline:none;'></td>" +
                            "<td style='padding: 10px 8px;'><input type='text' id='prod-img-" + p.id + "' value='" + (p.image_url || '') + "' placeholder='Link ảnh...' style='width:90px; height:28px; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:4px; color:white; padding:0 4px; font-size:11px; outline:none;'></td>" +
                            "<td style='padding: 10px 8px; text-align:right;'><input type='number' id='prod-price-" + p.id + "' value='" + p.price + "' style='width:90px; height:28px; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:4px; color:#86efac; text-align:right; padding-right:4px; font-weight:700; outline:none;'></td>" +
                            "<td style='padding: 10px 8px; text-align:center;'><input type='number' id='prod-stock-" + p.id + "' value='" + p.stock + "' style='width:70px; height:28px; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:4px; color:white; text-align:center; outline:none;'></td>" +
                            "<td style='padding: 10px 8px; text-align:center; display:flex; justify-content:center; gap:6px;'>" +
                                "<button onclick='updateProduct(" + p.id + ")' style='background:#10b981; color:white; border:none; padding:4px 10px; border-radius:4px; font-size:11px; cursor:pointer; font-weight:bold;'>Lưu</button>" +
                                "<button onclick='deleteProduct(" + p.id + ")' style='background:#ef4444; color:white; border:none; padding:4px 10px; border-radius:4px; font-size:11px; cursor:pointer; font-weight:bold;'>Xóa</button>" +
                            "</td>";
                        tbody.appendChild(tr);
                    });
                }
            };
            xhr.send();
        }

        function saveAllProducts() {
            if (!window.currentProdsList || window.currentProdsList.length === 0) {
                alert("Không có sản phẩm nào để lưu!");
                return;
            }
            
            var batchData = [];
            for (var i = 0; i < window.currentProdsList.length; i++) {
                var p = window.currentProdsList[i];
                var catEl = document.getElementById("prod-cat-" + p.id);
                var imgEl = document.getElementById("prod-img-" + p.id);
                var priceEl = document.getElementById("prod-price-" + p.id);
                var stockEl = document.getElementById("prod-stock-" + p.id);
                
                if (catEl && priceEl && stockEl) {
                    var category = catEl.value.trim() || "Thức uống";
                    var image_url = imgEl ? imgEl.value.trim() : "";
                    var price = parseFloat(priceEl.value || 0);
                    var stock = parseInt(stockEl.value || 0);
                    
                    if (price < 1000) {
                        alert("Đơn giá sản phẩm '" + p.name + "' phải từ 1.000 VNĐ trở lên!");
                        return;
                    }
                    if (stock < 0) {
                        alert("Số lượng tồn kho sản phẩm '" + p.name + "' không được âm!");
                        return;
                    }
                    
                    batchData.push({
                        id: p.id,
                        category: category,
                        image_url: image_url,
                        price: price,
                        stock: stock
                    });
                }
            }
            
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/products/batch-update", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var res = JSON.parse(xhr.responseText || "{}");
                    alert(res.message || "Đã lưu tất cả sản phẩm thành công!");
                    loadInventoryList();
                    if (typeof fetchPosProducts === "function") fetchPosProducts();
                } else {
                    alert("Lỗi khi lưu sản phẩm!");
                }
            };
            xhr.send(JSON.stringify({ items: batchData }));
        }

        function deleteSelectedProducts() {
            var selectedIds = [];
            var chks = document.querySelectorAll(".chk-prod:checked");
            chks.forEach(function(c) {
                selectedIds.push(parseInt(c.value));
            });
            
            if (selectedIds.length === 0) {
                alert("Vui lòng tích chọn ít nhất 1 sản phẩm để xóa!");
                return;
            }
            
            if (!confirm("Bạn có chắc chắn muốn xóa " + selectedIds.length + " sản phẩm đã chọn khỏi thực đơn?")) {
                return;
            }
            
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/products/batch-delete", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var res = JSON.parse(xhr.responseText || "{}");
                    alert(res.message || "Đã xóa các sản phẩm được chọn thành công!");
                    var master = document.getElementById("chk-all-prods");
                    if (master) master.checked = false;
                    loadInventoryList();
                    if (typeof fetchPosProducts === "function") fetchPosProducts();
                } else {
                    alert("Lỗi khi xóa sản phẩm!");
                }
            };
            xhr.send(JSON.stringify({ ids: selectedIds }));
        }

        function addNewProduct() {
            var name = document.getElementById("new-prod-name").value.trim();
            var categoryInput = document.getElementById("new-prod-category");
            var category = (categoryInput ? categoryInput.value.trim() : "") || "Thức uống";
            var price = parseFloat(document.getElementById("new-prod-price").value || 0);
            var stock = parseInt(document.getElementById("new-prod-stock").value || 0);
            var imageInput = document.getElementById("new-prod-image");
            var image_url = imageInput ? imageInput.value.trim() : "";
            
            if (!name) {
                alert("Vui lòng nhập tên sản phẩm!");
                return;
            }
            if (price < 1000) {
                alert("Đơn giá sản phẩm phải từ 1.000 VNĐ trở lên!");
                return;
            }
            if (stock < 0) {
                alert("Số lượng tồn kho không được âm!");
                return;
            }
            
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/products/add", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onload = function() {
                var res = JSON.parse(xhr.responseText || "{}");
                if (xhr.status === 200) {
                    alert(res.message || "Đã thêm sản phẩm thành công!");
                    document.getElementById("new-prod-name").value = "";
                    if (categoryInput) categoryInput.value = "";
                    document.getElementById("new-prod-price").value = "";
                    document.getElementById("new-prod-stock").value = "";
                    if (imageInput) imageInput.value = "";
                    loadInventoryList();
                    if (typeof fetchPosProducts === "function") fetchPosProducts();
                } else {
                    alert("Lỗi: " + (res.message || "Không thể thêm sản phẩm!"));
                }
            };
            xhr.onerror = function() {
                alert("Lỗi kết nối máy chủ!");
            };
            xhr.send(JSON.stringify({ name: name, category: category, price: price, stock: stock, image_url: image_url }));
        }

        function updateProduct(id) {
            var price = parseFloat(document.getElementById("prod-price-" + id).value || 0);
            var stock = parseInt(document.getElementById("prod-stock-" + id).value || 0);
            var image_url = document.getElementById("prod-img-" + id).value.trim();
            var category = document.getElementById("prod-cat-" + id).value.trim();
            
            if (price < 1000) {
                alert("Đơn giá sản phẩm phải từ 1000 VNĐ trở lên!");
                return;
            }
            if (stock < 0) {
                alert("Số lượng tồn kho không được âm!");
                return;
            }
            if (!category) {
                alert("Danh mục sản phẩm không được để trống!");
                return;
            }
            
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/products/update", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onload = function() {
                var res = JSON.parse(xhr.responseText);
                if (xhr.status === 200) {
                    alert("Cập nhật thành công!");
                    loadInventoryList();
                } else {
                    alert("Lỗi: " + res.message);
                }
            };
            xhr.send(JSON.stringify({ id: id, price: price, stock: stock, image_url: image_url, category: category }));
        }

        function deleteProduct(id) {
            if (!confirm("Bạn có chắc muốn xóa sản phẩm này khỏi thực đơn?")) return;
            
            var xhr = new XMLHttpRequest();
            xhr.open("DELETE", "/api/products/delete/" + id, true);
            xhr.onload = function() {
                var res = JSON.parse(xhr.responseText);
                if (xhr.status === 200) {
                    alert(res.message);
                    loadInventoryList();
                } else {
                    alert("Lỗi: " + res.message);
                }
            };
            xhr.send();
        }

        function switchInventoryTab(tabName) {
            document.getElementById('tab-content-products').style.display = tabName === 'products' ? 'block' : 'none';
            document.getElementById('tab-content-tables').style.display = tabName === 'tables' ? 'block' : 'none';
            
            var btnProd = document.getElementById('tab-btn-products');
            var btnTables = document.getElementById('tab-btn-tables');
            
            if (tabName === 'products') {
                btnProd.style.background = '#6366f1';
                btnProd.style.color = 'white';
                btnTables.style.background = 'transparent';
                btnTables.style.color = '#9ca3af';
                loadInventoryList();
            } else {
                btnTables.style.background = '#6366f1';
                btnTables.style.color = 'white';
                btnProd.style.background = 'transparent';
                btnProd.style.color = '#9ca3af';
                loadAdminTables();
            }
        }

        function loadAdminTables() {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/tables", true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var tables = JSON.parse(xhr.responseText);
                    var tbody = document.getElementById("inventory-tables-body");
                    if (!tbody) return;
                    tbody.innerHTML = "";
                    
                    if (tables.length === 0) {
                        tbody.innerHTML = "<tr><td colspan='6' style='color:#6b7280; padding:12px; text-align:center;'>Chưa có bàn bida nào</td></tr>";
                        return;
                    }
                    
                    tables.forEach(function(t) {
                        var tr = document.createElement("tr");
                        tr.style.borderBottom = "1px solid rgba(255,255,255,0.04)";
                        tr.innerHTML = 
                            "<td style='padding: 10px 8px; font-weight:600; color:white;'><input type='text' id='adm-table-name-" + t.id + "' value='" + t.name + "' style='width:120px; height:28px; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:4px; color:white; padding:0 6px; font-size:12px; outline:none;'></td>" +
                            "<td style='padding: 10px 8px; color:#a5b4fc;'>" + 
                                "<select id='adm-table-type-" + t.id + "' style='height:28px; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:4px; color:white; font-size:11px; outline:none;'>" +
                                    "<option value='LIP' " + (t.table_type === 'LIP' ? 'selected' : '') + ">Líp</option>" +
                                    "<option value='3C' " + (t.table_type === '3C' ? 'selected' : '') + ">3 Băng</option>" +
                                    "<option value='POOL' " + (t.table_type === 'POOL' ? 'selected' : '') + ">Lỗ</option>" +
                                "</select>" +
                            "</td>" +
                            "<td style='padding: 10px 8px;'>" +
                                "<select id='adm-table-tier-" + t.id + "' style='height:28px; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:4px; color:white; font-size:11px; outline:none;'>" +
                                    "<option value='STANDARD' " + (t.table_tier === 'STANDARD' ? 'selected' : '') + ">Thường</option>" +
                                    "<option value='VIP' " + (t.table_tier === 'VIP' ? 'selected' : '') + ">VIP</option>" +
                                "</select>" +
                            "</td>" +
                            "<td style='padding: 10px 8px;'><input type='text' id='adm-table-cam-" + t.id + "' value='" + (t.camera_url || '') + "' placeholder='Cam ID' style='width:70px; height:28px; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:4px; color:white; padding:0 4px; font-size:11px; outline:none;'></td>" +
                            "<td style='padding: 10px 8px; text-align:right;'><input type='number' id='adm-table-price-" + t.id + "' value='" + t.price_per_hour + "' style='width:90px; height:28px; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:4px; color:#86efac; text-align:right; padding-right:4px; font-weight:700; outline:none;'></td>" +
                            "<td style='padding: 10px 8px; text-align:center; display:flex; justify-content:center; gap:6px;'>" +
                                "<button onclick='updateAdminTable(" + t.id + ")' style='background:#10b981; color:white; border:none; padding:4px 10px; border-radius:4px; font-size:11px; cursor:pointer; font-weight:bold;'>Lưu</button>" +
                                "<button onclick='deleteAdminTable(" + t.id + ")' style='background:#ef4444; color:white; border:none; padding:4px 10px; border-radius:4px; font-size:11px; cursor:pointer; font-weight:bold;'>Xóa</button>" +
                            "</td>";
                        tbody.appendChild(tr);
                    });
                }
            };
            xhr.send();
        }

        function addNewAdminTable() {
            var name = document.getElementById("new-table-name").value.trim();
            var type = document.getElementById("new-table-type").value;
            var tier = document.getElementById("new-table-tier").value;
            var price = parseFloat(document.getElementById("new-table-price").value || 50000);
            var cam = document.getElementById("new-table-cam").value.trim();
            
            if (!name) {
                alert("Vui lòng nhập tên bàn!");
                return;
            }
            
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/admin/tables/add", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onload = function() {
                var res = JSON.parse(xhr.responseText);
                if (xhr.status === 200) {
                    alert(res.message);
                    document.getElementById("new-table-name").value = "";
                    document.getElementById("new-table-price").value = "";
                    document.getElementById("new-table-cam").value = "";
                    loadAdminTables();
                    loadTables(); // Reload main dashboard tables
                } else {
                    alert("Lỗi: " + res.message);
                }
            };
            xhr.send(JSON.stringify({ name: name, table_type: type, table_tier: tier, price_per_hour: price, camera_url: cam }));
        }

        function updateAdminTable(id) {
            var name = document.getElementById("adm-table-name-" + id).value.trim();
            var type = document.getElementById("adm-table-type-" + id).value;
            var tier = document.getElementById("adm-table-tier-" + id).value;
            var price = parseFloat(document.getElementById("adm-table-price-" + id).value || 50000);
            var cam = document.getElementById("adm-table-cam-" + id).value.trim();
            
            if (!name) {
                alert("Tên bàn không được trống!");
                return;
            }
            
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/admin/tables/update", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onload = function() {
                var res = JSON.parse(xhr.responseText);
                if (xhr.status === 200) {
                    alert(res.message);
                    loadAdminTables();
                    loadTables(); // Reload main dashboard tables
                } else {
                    alert("Lỗi: " + res.message);
                }
            };
            xhr.send(JSON.stringify({ id: id, name: name, table_type: type, table_tier: tier, price_per_hour: price, camera_url: cam }));
        }

        function deleteAdminTable(id) {
            if (!confirm("Bạn có chắc chắn muốn xóa bàn này khỏi hệ thống?")) return;
            
            var xhr = new XMLHttpRequest();
            xhr.open("DELETE", "/api/admin/tables/" + id, true);
            xhr.onload = function() {
                var res = JSON.parse(xhr.responseText);
                if (xhr.status === 200) {
                    alert(res.message);
                    loadAdminTables();
                    loadTables(); // Reload main dashboard tables
                } else {
                    alert("Lỗi: " + res.message);
                }
            };
            xhr.send();
        }

        function showTableQRModal(tableId, tableName, token) {
            var qrTitle = document.getElementById("qr-modal-title");
            var qrImg = document.getElementById("qr-modal-image");
            var qrLink = document.getElementById("qr-modal-link");
            var targetUrl = window.location.origin + "/menu/" + tableId + "/" + token;
            
            qrTitle.textContent = "📷 MÃ QR GỌI MÓN - " + tableName;
            qrLink.textContent = targetUrl;
            qrImg.src = "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + encodeURIComponent(targetUrl);
            document.getElementById("qr-modal").style.display = "flex";
        }
        
        function closeQRModal() {
            document.getElementById("qr-modal").style.display = "none";
        }

        function approveCustomerOrder(card, tableId, items) {
            var btns = card.querySelectorAll("button");
            for (var i = 0; i < btns.length; i++) { btns[i].disabled = true; }
            
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/session/add-items/" + tableId, true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var resolvedEl = document.createElement("div");
                    resolvedEl.className = "event-resolved resolved-confirmed";
                    resolvedEl.textContent = "Đã duyệt món & thêm vào Bill";
                    card.style.borderLeftColor = "#22c55e";
                    
                    var actionsDiv = card.querySelector(".event-actions");
                    if (actionsDiv) actionsDiv.style.display = "none";
                    card.appendChild(resolvedEl);
                    loadTables();
                } else {
                    alert("Lỗi duyệt món: " + xhr.statusText);
                    for (var i = 0; i < btns.length; i++) { btns[i].disabled = false; }
                }
            };
            xhr.send(JSON.stringify({ items: items }));
        }

        // === HANDLE ACTION ===
        function handleAction(card, action) {
            var btns = card.querySelectorAll("button");
            for (var i = 0; i < btns.length; i++) { btns[i].disabled = true; }

            var resolvedEl = document.createElement("div");
            resolvedEl.className = "event-resolved";

            if (action === "confirm") {
                resolvedEl.className += " resolved-confirmed";
                // Neu la event Khach Order thi ghi la Da phuc vu xong
                var badgeEl = card.querySelector(".event-badge");
                if (badgeEl && badgeEl.textContent === "KHÁCH ORDER") {
                    resolvedEl.textContent = "ĐÃ PHỤC VỤ XONG";
                } else {
                    resolvedEl.textContent = "DA XAC NHAN - Nhan vien dang phuc vu";
                }
                card.style.borderLeftColor = "#22c55e";
            } else {
                resolvedEl.className += " resolved-dismissed";
                resolvedEl.textContent = "Hoan tat";
                card.style.opacity = "0.5";
            }

            var actionsDiv = card.querySelector(".event-actions");
            if (actionsDiv) actionsDiv.style.display = "none";
            card.appendChild(resolvedEl);
        }

        var lastEventId = "";

        // === RENDER EVENT ===
        function renderEvent(data) {
            if (!data || !data.event_type) return;
            // Bo qua cac tin nhan khach vay tay goi mon bang AI Camera
            if (data.event_type === "HAND_RAISED") return;
            // De-duplicate bang unique event ID de tranh spam polling
            if (data.id) {
                if (data.id === lastEventId) return;
                lastEventId = data.id;
            } else {
                if (data.image && data.image === lastImage) return;
                lastImage = data.image || "";
            }

            if (emptyState) { emptyState.style.display = "none"; }

            eventCount++;
            eventCountEl.textContent = eventCount;

            // Load lai du lieu ban khi co hoat dong tu AI
            loadTables();

            var card = document.createElement("div");
            card.className = "event-card";
            if (data.event_type === "HAND_RAISED") {
                card.className += " urgent";
            } else if (data.event_type === "CUSTOMER_ORDER") {
                card.style.borderLeftColor = "#f59e0b";
            }

            // Header
            var header = document.createElement("div");
            header.className = "event-header";

            var badge = document.createElement("span");
            badge.className = "event-badge";
            if (data.event_type === "HAND_RAISED") {
                badge.className += " badge-hand";
                badge.textContent = "KHACH VAY TAY";
            } else if (data.event_type === "CUSTOMER_ORDER") {
                badge.className += " badge-hand";
                badge.style.background = "#f59e0b";
                badge.textContent = "KHÁCH ORDER";
            } else if (data.event_type === "TABLE_EMPTY" || data.event_type === "TABLE_ACTIVE") {
                badge.style.display = "none";
            } else {
                badge.className += " badge-motion";
                badge.textContent = data.event_type;
            }

            var timeEl = document.createElement("span");
            timeEl.className = "event-time";
            timeEl.textContent = new Date().toLocaleTimeString();

            header.appendChild(badge);
            header.appendChild(timeEl);
            card.appendChild(header);

            // Message
            var msg = document.createElement("div");
            msg.className = "event-message";
            msg.textContent = data.message || ("Su kien: " + data.event_type + " tai Ban " + data.table_id);
            card.appendChild(msg);

            // Hien thi so dien thoai khach
            if (data.event_type === "CUSTOMER_ORDER" && data.phone) {
                var phoneDiv = document.createElement("div");
                phoneDiv.style.cssText = "margin-top: 4px; font-size: 13px; color: #86efac; font-weight: 700;";
                phoneDiv.innerHTML = "📞 SĐT khách: <span style='font-family: monospace;'>" + data.phone + "</span>";
                card.appendChild(phoneDiv);
            }

            // Ghi chu yeu cau cua khach
            if (data.event_type === "CUSTOMER_ORDER" && data.note) {
                var noteDiv = document.createElement("div");
                noteDiv.style.cssText = "margin-top: 6px; font-size: 13px; color: #fcd34d; font-weight: 600; padding: 6px 10px; background: rgba(245, 158, 11, 0.1); border-left: 3px solid #fbbf24; border-radius: 4px;";
                noteDiv.textContent = "📝 Ghi chú: " + data.note;
                card.appendChild(noteDiv);
            }

            // Customer Order items list inside card
            if (data.event_type === "CUSTOMER_ORDER" && data.items && data.items.length > 0) {
                var hasPaidItem = data.items.some(function(i) { return i.price > 0; });
                var listTitle = hasPaidItem ? "<b>Đồ khách đặt (Đã tự động thêm vào Bill):</b>" : "<b>Khách đã yêu cầu:</b>";
                var itemsDiv = document.createElement("div");
                itemsDiv.style.cssText = "margin: 10px 0; padding: 10px 14px; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; font-size: 13px; color: #e5e7eb;";
                var listHtml = listTitle + "<ul style='margin-left: 20px; margin-top: 4px; display: flex; flex-direction: column; gap: 4px;'>";
                data.items.forEach(function(item) {
                    if (item.price > 0) {
                        listHtml += "<li>" + item.item_name + " x" + item.quantity + " (" + Math.ceil(item.price * item.quantity).toLocaleString("vi-VN") + " đ)</li>";
                    } else {
                        listHtml += "<li style='color: #fbbf24;'>" + item.item_name + "</li>";
                    }
                });
                listHtml += "</ul>";
                itemsDiv.innerHTML = listHtml;
                card.appendChild(itemsDiv);
            }

            // Play statistics section in card
            if (data.date || data.play_time || data.total_fee) {
                var statsContainer = document.createElement("div");
                statsContainer.style.cssText = "margin-bottom: 14px; padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; font-size: 12px; color: #8b949e; line-height: 1.5; display: flex; flex-direction: column; gap: 4px;";
                
                if (data.date) {
                    statsContainer.innerHTML += "<div>Ngày tạo: <b style='color: white;'>" + data.date + "</b></div>";
                }
                if (data.play_time) {
                    statsContainer.innerHTML += "<div>Thời gian đã chơi: <b style='color: #fbbf24;'>" + data.play_time + "</b></div>";
                }
                if (data.total_fee) {
                    statsContainer.innerHTML += "<div>Tổng tiền chơi hiện tại: <b style='color: #22c55e;'>" + data.total_fee + "</b></div>";
                }
                card.appendChild(statsContainer);
            }

            // Image
            if (data.image) {
                var img = document.createElement("img");
                img.className = "event-image";
                img.src = data.image;
                img.alt = "AI Camera Capture";
                card.appendChild(img);
            }

            // Action buttons for both AI alerts and Customer Orders
            if (data.image || data.event_type === "CUSTOMER_ORDER") {
                var actions = document.createElement("div");
                actions.className = "event-actions";

                if (data.event_type === "CUSTOMER_ORDER") {
                    var isTransferRequest = false;
                    var requestedType = null;
                    if (data.items && data.items.length > 0) {
                        data.items.forEach(function(i) {
                            if (i.item_name && i.item_name.startsWith("Đổi sang bàn")) {
                                isTransferRequest = true;
                                if (i.item_name.includes("Líp")) requestedType = "LIP";
                                else if (i.item_name.includes("Băng")) requestedType = "3C";
                                else if (i.item_name.includes("Lỗ")) requestedType = "POOL";
                            }
                        });
                    }

                    if (isTransferRequest) {
                        var btnApprove = document.createElement("button");
                        btnApprove.className = "btn btn-confirm";
                        btnApprove.style.background = "linear-gradient(135deg, #10b981, #059669)";
                        btnApprove.style.flex = "1";
                        btnApprove.innerHTML = "&#10004; Xác nhận";
                        btnApprove.addEventListener("click", function() {
                            showTransferModal(data.table_id, requestedType);
                            handleAction(card, "confirm");
                        });

                        var btnReject = document.createElement("button");
                        btnReject.className = "btn btn-dismiss";
                        btnReject.style.flex = "1";
                        btnReject.innerHTML = "&#10008; Từ chối";
                        btnReject.addEventListener("click", function() {
                            showRejectTransferModal(data.table_id);
                            handleAction(card, "dismiss");
                        });

                        actions.appendChild(btnApprove);
                        actions.appendChild(btnReject);
                    } else {
                        var btnApprove = document.createElement("button");
                        btnApprove.className = "btn btn-confirm";
                        btnApprove.style.background = "linear-gradient(135deg, #10b981, #059669)";
                        btnApprove.style.flex = "1";
                        btnApprove.innerHTML = "&#10004; Xác nhận đã phục vụ";
                        btnApprove.addEventListener("click", function() {
                            handleAction(card, "confirm");
                        });
                        actions.appendChild(btnApprove);
                    }
                } else {
                    var btnConfirm = document.createElement("button");
                    btnConfirm.className = "btn btn-confirm";
                    btnConfirm.innerHTML = "&#10004; Chay ra phuc vu";
                    btnConfirm.addEventListener("click", function() {
                        handleAction(card, "confirm");
                    });

                    var btnDismiss = document.createElement("button");
                    btnDismiss.className = "btn btn-dismiss";
                    btnDismiss.innerHTML = "&#10006; Bo qua (Bao gia)";
                    btnDismiss.addEventListener("click", function() {
                        handleAction(card, "dismiss");
                    });

                    actions.appendChild(btnConfirm);
                    actions.appendChild(btnDismiss);
                }

                actions.style.cssText = "display: flex; gap: 8px; margin-top: 10px;";
                card.appendChild(actions);
                if (data.event_type === "CUSTOMER_ORDER") {
                    playOrderAlert();
                } else {
                    playAlert();
                }
            }

            eventsDiv.insertBefore(card, eventsDiv.firstChild);
        }

        // === WEBSOCKET CONNECTION ===
        function connectWebSocket() {
            try {
                var wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
                var wsUrl = wsProtocol + "//" + window.location.host + "/ws/admin";
                
                bannerText.textContent = "Đang mở WebSocket tới: " + wsUrl;
                
                var ws = new WebSocket(wsUrl);
                
                ws.onopen = function() {
                    statusDot.className = "dot dot-green";
                    statusLabel.textContent = "Dang hoat dong";
                    statusBanner.className = "status-banner status-connected";
                    bannerIcon.innerHTML = "&#9889;";
                    bannerText.textContent = "He thong dang hoat dong - AI Camera dang giam sat (WebSocket Live)";
                };
                
                ws.onmessage = function(event) {
                    try {
                        var data = JSON.parse(event.data);
                        if (data && data.event_type) {
                            renderEvent(data);
                        }
                    } catch(e) {}
                };
                
                ws.onclose = function(e) {
                    statusDot.className = "dot dot-red";
                    statusLabel.textContent = "Mat ket noi";
                    statusBanner.className = "status-banner status-error";
                    bannerIcon.innerHTML = "&#9888;";
                    bannerText.textContent = "Mất kết nối (" + e.code + "). Đang thử lại...";
                    setTimeout(connectWebSocket, 3000);
                };
                
                ws.onerror = function(err) {
                    statusDot.className = "dot dot-red";
                    statusBanner.className = "status-banner status-error";
                    bannerText.textContent = "Lỗi đường truyền WebSocket. Vui lòng F5!";
                };
            } catch(ex) {
                bannerText.textContent = "JS Error: " + ex.message;
            }
        }

        connectWebSocket();

        // === HIGHLIGHT CLIP FUNCTIONS ===
        var clipStatusDiv = document.getElementById("clip-status");
        var clipBtn = document.getElementById("clip-btn");
        var clipsListDiv = document.getElementById("clips-list");
        var timeInput = document.getElementById("time-input");
        var pastClipBtn = document.getElementById("past-clip-btn");

        // Dien gio hien tai lam goi y cho Time Machine
        var now = new Date();
        var currentHours = now.getHours();
        var currentMinutes = now.getMinutes();
        timeInput.value = (currentHours < 10 ? "0" + currentHours : currentHours) + ":" + (currentMinutes < 10 ? "0" + currentMinutes : currentMinutes);

        function requestClip(tableId) {
            clipBtn.disabled = true;
            clipBtn.textContent = "Dang xu ly...";
            clipStatusDiv.style.display = "block";
            clipStatusDiv.className = "highlight-status highlight-processing";
            clipStatusDiv.textContent = "AI dang cat 30 giay gan nhat thanh video... Vui long doi 5-10 giay.";

            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/clip/" + tableId, true);
            xhr.onload = function() {
                var checkCount = 0;
                var checkInterval = setInterval(function() {
                    checkCount++;
                    var xhr2 = new XMLHttpRequest();
                    xhr2.open("GET", "/api/clip-status/" + tableId + "?_=" + Date.now(), true);
                    xhr2.onload = function() {
                        if (xhr2.status === 200) {
                            var result = JSON.parse(xhr2.responseText);
                            if (result.status === "ready") {
                                clearInterval(checkInterval);
                                clipStatusDiv.className = "highlight-status highlight-ready";
                                clipStatusDiv.innerHTML = "";

                                var readyText = document.createElement("span");
                                readyText.textContent = "Clip 30s da san sang! ";
                                clipStatusDiv.appendChild(readyText);

                                var downloadLink = document.createElement("a");
                                downloadLink.href = result.url;
                                downloadLink.download = result.filename;
                                downloadLink.className = "btn btn-download";
                                downloadLink.style.display = "inline-flex";
                                downloadLink.style.marginLeft = "10px";
                                downloadLink.style.padding = "6px 14px";
                                downloadLink.style.fontSize = "12px";
                                downloadLink.innerHTML = "&#11015; Tai ve MP4";
                                clipStatusDiv.appendChild(downloadLink);

                                clipBtn.disabled = false;
                                clipBtn.innerHTML = "🎥 Highlight 30s bàn đã chọn";
                                loadClips();
                                playAlert();
                            }
                        }
                    };
                    xhr2.send();

                    if (checkCount > 30) {
                        clearInterval(checkInterval);
                        clipStatusDiv.className = "highlight-status highlight-processing";
                        clipStatusDiv.textContent = "Qua lau - Hay thu lai.";
                        clipBtn.disabled = false;
                        clipBtn.innerHTML = "🎥 Highlight 30s bàn đã chọn";
                    }
                }, 1000);
            };
            xhr.send();
        }

        // Trich xuat clip tu Time Machine trong qua khu
        function requestPastClip(tableId) {
            var selectedTime = timeInput.value;
            if (!selectedTime) {
                alert("Vui long chon thoi gian can lay highlight!");
                return;
            }

            pastClipBtn.disabled = true;
            pastClipBtn.textContent = "Dang lay...";
            clipStatusDiv.style.display = "block";
            clipStatusDiv.className = "highlight-status highlight-processing";
            clipStatusDiv.textContent = "Co may thoi gian dang tim kiem va trich xuat video luc " + selectedTime + "...";

            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/highlight-past/" + tableId, true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onload = function() {
                pastClipBtn.disabled = false;
                pastClipBtn.innerHTML = "⌛ Trích xuất clip";

                if (xhr.status === 200) {
                    var result = JSON.parse(xhr.responseText);
                    clipStatusDiv.className = "highlight-status highlight-ready";
                    clipStatusDiv.innerHTML = "";

                    var readyText = document.createElement("span");
                    readyText.textContent = "Highlight luc " + selectedTime + " da san sang! ";
                    clipStatusDiv.appendChild(readyText);

                    var downloadLink = document.createElement("a");
                    downloadLink.href = result.url;
                    downloadLink.download = result.filename;
                    downloadLink.className = "btn btn-download";
                    downloadLink.style.display = "inline-flex";
                    downloadLink.style.marginLeft = "10px";
                    downloadLink.style.padding = "6px 14px";
                    downloadLink.style.fontSize = "12px";
                    downloadLink.innerHTML = "&#11015; Tai video " + selectedTime;
                    clipStatusDiv.appendChild(downloadLink);

                    loadClips();
                    playAlert();
                } else {
                    var errorMsg = "Khong tim thay video luu tru cho thoi gian nay!";
                    try {
                        var res = JSON.parse(xhr.responseText);
                        if (res && res.message) errorMsg = res.message;
                    } catch(e) {}
                    
                    clipStatusDiv.className = "highlight-status highlight-processing";
                    clipStatusDiv.style.background = "rgba(239,68,68,0.15)";
                    clipStatusDiv.style.borderColor = "rgba(239,68,68,0.3)";
                    clipStatusDiv.style.color = "#fca5a5";
                    clipStatusDiv.textContent = "❌ " + errorMsg;
                }
            };
            xhr.onerror = function() {
                pastClipBtn.disabled = false;
                pastClipBtn.innerHTML = "⌛ Trích xuất clip";
                clipStatusDiv.className = "highlight-status highlight-processing";
                clipStatusDiv.textContent = "Loi ket noi toi Server.";
            };
            xhr.send(JSON.stringify({ "time": selectedTime }));
        }

        // Xoa clip highlight
        function deleteClip(filename) {
            var xhr = new XMLHttpRequest();
            xhr.open("DELETE", "/api/clip/" + filename, true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    loadClips();
                } else {
                    alert("Khong the xoa clip!");
                }
            };
            xhr.send();
        }

        function loadClips() {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/clips?_=" + Date.now(), true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var clips = JSON.parse(xhr.responseText);
                    clipsListDiv.innerHTML = "";
                    if (clips.length === 0) return;

                    var title = document.createElement("div");
                    title.style.cssText = "font-size:12px; font-weight:600; color:#8b949e; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;";
                    title.textContent = "Clip da luu";
                    clipsListDiv.appendChild(title);

                    for (var i = 0; i < clips.length && i < 5; i++) {
                        var item = document.createElement("div");
                        item.className = "clip-item";

                        var nameSpan = document.createElement("span");
                        nameSpan.className = "clip-item-name";
                        nameSpan.textContent = clips[i].filename;
                        item.appendChild(nameSpan);

                        var rightDiv = document.createElement("div");
                        rightDiv.style.display = "flex";
                        rightDiv.style.alignItems = "center";
                        rightDiv.style.gap = "10px";

                        var sizeSpan = document.createElement("span");
                        sizeSpan.className = "clip-item-size";
                        sizeSpan.textContent = clips[i].size_mb + " MB";
                        rightDiv.appendChild(sizeSpan);

                        // Nut download
                        var dlBtn = document.createElement("a");
                        dlBtn.href = clips[i].url;
                        dlBtn.download = clips[i].filename;
                        dlBtn.className = "btn btn-download";
                        dlBtn.style.padding = "4px 12px";
                        dlBtn.style.fontSize = "11px";
                        dlBtn.style.borderRadius = "6px";
                        dlBtn.innerHTML = "&#11015; Tai";
                        rightDiv.appendChild(dlBtn);

                        // Nut xoa clip
                        var delBtn = document.createElement("button");
                        delBtn.className = "btn btn-dismiss";
                        delBtn.style.padding = "4px 12px";
                        delBtn.style.fontSize = "11px";
                        delBtn.style.borderRadius = "6px";
                        delBtn.style.marginLeft = "2px";
                        delBtn.innerHTML = "&#128465; Xoa";
                        delBtn.setAttribute("data-filename", clips[i].filename);
                        delBtn.addEventListener("click", function() {
                            var fname = this.getAttribute("data-filename");
                            if (confirm("Ban co chac muon xoa clip: " + fname + "?")) {
                                deleteClip(fname);
                            }
                        });
                        rightDiv.appendChild(delBtn);

                        item.appendChild(rightDiv);
                        clipsListDiv.appendChild(item);
                    }
                }
            };
            xhr.send();
        }

        // === POS MODAL LOGIC ===
        var posProducts = [];
        var posCart = {}; // { id: { name, price, qty, img } }
        var posCurrentTableId = null;

        function openPosModal(tableId, tableName) {
            posCurrentTableId = tableId;
            document.getElementById("pos-title").textContent = "🛒 Thu Ngân Gọi Món - Bàn " + tableName;
            document.getElementById("pos-modal").style.display = "flex";
            posCart = {};
            renderPosCart();
            
            if (posProducts.length === 0) {
                fetchPosProducts();
            } else {
                renderPosCategories();
            }
        }

        function closePosModal() {
            document.getElementById("pos-modal").style.display = "none";
        }

        function fetchPosProducts() {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/products", true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    posProducts = JSON.parse(xhr.responseText);
                    

                    
                    renderPosCategories();
                }
            };
            xhr.send();
        }

        function renderPosCategories() {
            var catContainer = document.getElementById("pos-categories");
            catContainer.innerHTML = "";
            
            var categories = ["Tất cả"];
            posProducts.forEach(function(p) {
                if (p.category && categories.indexOf(p.category) === -1) {
                    categories.push(p.category);
                }
            });
            
            categories.forEach(function(cat, index) {
                var btn = document.createElement("button");
                btn.className = "cat-btn" + (index === 0 ? " active" : "");
                btn.style.cssText = "padding: 8px 16px; border-radius: 8px; border: none; background: " + (index === 0 ? "#10b981" : "rgba(255,255,255,0.1)") + "; color: white; cursor: pointer; white-space: nowrap; font-weight: bold;";
                btn.textContent = cat;
                btn.onclick = function() {
                    var btns = catContainer.querySelectorAll("button");
                    for (var i = 0; i < btns.length; i++) {
                        btns[i].style.background = "rgba(255,255,255,0.1)";
                    }
                    btn.style.background = "#10b981";
                    renderPosProducts(cat);
                };
                catContainer.appendChild(btn);
            });
            
            renderPosProducts("Tất cả");
        }

        function renderPosProducts(category) {
            var prodContainer = document.getElementById("pos-products");
            prodContainer.innerHTML = "";
            
            posProducts.forEach(function(p) {
                if (category !== "Tất cả" && p.category !== category) return;
                
                var card = document.createElement("div");
                card.style.cssText = "background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 12px; cursor: pointer; display: flex; flex-direction: column; gap: 8px; transition: transform 0.2s, background 0.2s;";
                card.onmouseover = function() { this.style.transform = "translateY(-2px)"; this.style.background = "rgba(255,255,255,0.08)"; };
                card.onmouseout = function() { this.style.transform = "translateY(0)"; this.style.background = "rgba(255,255,255,0.05)"; };
                card.onclick = function() { addToPosCart(p); };
                
                if (p.image_url) {
                    var img = document.createElement("img");
                    img.src = p.image_url;
                    img.style.cssText = "width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 8px;";
                    img.onerror = function() { this.style.display = "none"; };
                    card.appendChild(img);
                } else {
                    var placeholder = document.createElement("div");
                    placeholder.style.cssText = "width: 100%; aspect-ratio: 1; background: rgba(0,0,0,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; color: rgba(255,255,255,0.2);";
                    placeholder.innerHTML = "&#127864;";
                    card.appendChild(placeholder);
                }
                
                var nameDiv = document.createElement("div");
                nameDiv.style.cssText = "font-weight: 600; font-size: 14px; color: white; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;";
                nameDiv.textContent = p.name;
                card.appendChild(nameDiv);
                
                var priceDiv = document.createElement("div");
                priceDiv.style.cssText = "color: #34d399; font-weight: bold; font-size: 13px;";
                priceDiv.textContent = p.price.toLocaleString("vi-VN") + "đ";
                card.appendChild(priceDiv);
                    
                prodContainer.appendChild(card);
            });
        }

        function addToPosCart(p) {
            if (posCart[p.id]) {
                posCart[p.id].qty += 1;
            } else {
                posCart[p.id] = { id: p.id, name: p.name, price: p.price, qty: 1 };
            }
            renderPosCart();
        }

        window.updatePosCartQty = function(id, delta) {
            if (posCart[id]) {
                posCart[id].qty += delta;
                if (posCart[id].qty <= 0) {
                    delete posCart[id];
                }
                renderPosCart();
            }
        };

        function renderPosCart() {
            var cartContainer = document.getElementById("pos-cart-items");
            cartContainer.innerHTML = "";
            var total = 0;
            var hasItems = false;
            
            var keys = Object.keys(posCart);
            for (var i = 0; i < keys.length; i++) {
                hasItems = true;
                var item = posCart[keys[i]];
                var itemTotal = item.price * item.qty;
                total += itemTotal;
                
                var row = document.createElement("div");
                row.style.cssText = "display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px;";
                
                var infoDiv = document.createElement("div");
                infoDiv.style.cssText = "flex: 1; display: flex; flex-direction: column; gap: 4px;";
                
                var nameDiv = document.createElement("div");
                nameDiv.style.cssText = "font-weight: bold; font-size: 13px; color: white;";
                nameDiv.textContent = item.name;
                infoDiv.appendChild(nameDiv);
                
                var priceDiv = document.createElement("div");
                priceDiv.style.cssText = "color: #9ca3af; font-size: 12px;";
                priceDiv.textContent = item.price.toLocaleString("vi-VN") + "\u0111";
                infoDiv.appendChild(priceDiv);
                
                row.appendChild(infoDiv);
                
                var qtyDiv = document.createElement("div");
                qtyDiv.style.cssText = "display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.1); border-radius: 6px; padding: 2px;";
                
                var btnMinus = document.createElement("button");
                btnMinus.style.cssText = "background: transparent; border: none; color: white; width: 24px; height: 24px; cursor: pointer; font-weight: bold;";
                btnMinus.textContent = "-";
                btnMinus.setAttribute("data-id", item.id);
                btnMinus.onclick = function() { updatePosCartQty(this.getAttribute("data-id"), -1); };
                qtyDiv.appendChild(btnMinus);
                
                var qtySpan = document.createElement("span");
                qtySpan.style.cssText = "font-weight: bold; font-size: 13px; min-width: 16px; text-align: center; color: white;";
                qtySpan.textContent = item.qty;
                qtyDiv.appendChild(qtySpan);
                
                var btnPlus = document.createElement("button");
                btnPlus.style.cssText = "background: transparent; border: none; color: white; width: 24px; height: 24px; cursor: pointer; font-weight: bold;";
                btnPlus.textContent = "+";
                btnPlus.setAttribute("data-id", item.id);
                btnPlus.onclick = function() { updatePosCartQty(this.getAttribute("data-id"), 1); };
                qtyDiv.appendChild(btnPlus);
                
                row.appendChild(qtyDiv);
                cartContainer.appendChild(row);
            }
            
            if (!hasItems) {
                var emptyMsg = document.createElement("div");
                emptyMsg.style.cssText = "text-align: center; color: #6b7280; font-style: italic; margin-top: 20px;";
                emptyMsg.textContent = "Ch\u01b0a c\u00f3 m\u00f3n n\u00e0o";
                cartContainer.appendChild(emptyMsg);
            }
            
            document.getElementById("pos-total-price").textContent = total.toLocaleString("vi-VN") + "\u0111";
        }

        function submitPosOrder() {
            var itemsList = [];
            var keys = Object.keys(posCart);
            for (var i = 0; i < keys.length; i++) {
                var item = posCart[keys[i]];
                itemsList.push({
                    name: item.name,
                    item_name: item.name,
                    qty: item.qty,
                    quantity: item.qty,
                    price: item.price
                });
            }
            
            if (itemsList.length === 0) {
                alert("Giỏ hàng trống!");
                return;
            }
            
            var btn = document.getElementById("pos-submit-btn");
            btn.textContent = "⏳ Đang thêm vào hóa đơn...";
            btn.disabled = true;
            
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/session/add-items/" + posCurrentTableId, true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onload = function() {
                btn.textContent = "🛒 Xác nhận thêm vào Bàn";
                btn.disabled = false;
                if (xhr.status === 200) {
                    var res = JSON.parse(xhr.responseText || "{}");
                    alert(res.message || "Đã thêm món vào hóa đơn bàn thành công!");
                    posCart = {};
                    renderPosCart();
                    closePosModal();
                    loadTables(); // Refresh dashboard table cards
                    if (typeof fetchPosProducts === "function") fetchPosProducts();
                } else {
                    var errMsg = "Lỗi khi gọi món!";
                    try {
                        var res = JSON.parse(xhr.responseText);
                        if (res && res.message) errMsg = res.message;
                    } catch(e) {}
                    alert("Lỗi: " + errMsg);
                }
            };
            xhr.onerror = function() {
                btn.textContent = "🛒 Xác nhận thêm vào Bàn";
                btn.disabled = false;
                alert("Lỗi kết nối máy chủ!");
            };
            xhr.send(JSON.stringify({ items: itemsList }));
        }

        // Load ban dau
        loadClips();
        loadTables();
    </script>

</body>
</html>"""
