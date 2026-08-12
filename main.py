import streamlit as st
import streamlit.components.v1 as components

# Config Halaman Streamlit
st.set_page_config(
    page_title="Ruang Teduh - Schedule Matrix",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Sembunyikan Header & Footer Bawaan Streamlit
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

# HTML + CSS + JS Murni untuk Tampilan Mewah
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ruang Teduh - Schedule Matrix</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --gold-primary: #f59e0b;
            --gold-light: #fbbf24;
            --text-white: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #334155;
            --blue-badge: #1e3a8a;
            --blue-text: #60a5fa;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-white);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 15px;
        }

        .header-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }

        .pill-tag {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.3);
            color: var(--gold-light);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 12px;
        }

        .title {
            font-size: 26px;
            font-weight: 800;
            color: var(--text-white);
            margin: 0 0 8px 0;
            line-height: 1.2;
        }

        .subtitle {
            font-size: 14px;
            color: var(--text-muted);
            margin: 0 0 20px 0;
        }

        .btn-download {
            background: linear-gradient(135deg, var(--gold-primary), #d97706);
            color: #000;
            font-weight: 700;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            box-shadow: 0 4px 14px rgba(245, 158, 11, 0.4);
            transition: all 0.2s ease;
            text-decoration: none;
        }

        .btn-download:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.6);
        }

        /* Filter Tabs */
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            overflow-x: auto;
            padding-bottom: 5px;
        }

        .tab-btn {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 10px 18px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            white-space: nowrap;
        }

        .tab-btn.active {
            background: rgba(245, 158, 11, 0.15);
            border-color: var(--gold-primary);
            color: var(--gold-light);
        }

        /* Table Styling */
        .table-container {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            overflow-x: auto;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 13px;
        }

        th {
            background: #0f172a;
            color: var(--gold-light);
            font-weight: 700;
            text-transform: uppercase;
            padding: 14px 16px;
            border-bottom: 1px solid var(--border-color);
            letter-spacing: 0.5px;
        }

        td {
            padding: 14px 16px;
            border-bottom: 1px solid var(--border-color);
            color: #e2e8f0;
            vertical-align: middle;
        }

        tr:last-child td {
            border-bottom: none;
        }

        .time-badge {
            background: rgba(30, 58, 138, 0.6);
            color: var(--blue-text);
            border: 1px solid rgba(96, 165, 250, 0.3);
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: 700;
            display: inline-block;
        }

        .playlist-badge {
            background: rgba(245, 158, 11, 0.1);
            color: var(--gold-light);
            border: 1px solid rgba(245, 158, 11, 0.3);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }

        .hashtag {
            color: var(--gold-light);
            font-size: 11px;
            opacity: 0.8;
        }
    </style>
</head>
<body>

    <div class="header-card">
        <div class="pill-tag">🌿 Ruang Teduh – Schedule Matrix</div>
        <h1 class="title">Spreadsheet Gebrakan Emas (3 Hari)</h1>
        <p class="subtitle">Jadwal posting terstruktur Siang, Sore & Malam | 15 Konten Serial TikTok Mode Slide</p>
        <button class="btn-download" onclick="downloadCSV()">📄 Download Excel (.csv)</button>
    </div>

    <div class="tabs">
        <button class="tab-btn active" onclick="filterTable('all', this)">Semua Hari (15 Postingan)</button>
        <button class="tab-btn" onclick="filterTable('rabu', this)">Rabu (Ciri Wanita Ahli Surga)</button>
        <button class="tab-btn" onclick="filterTable('kamis', this)">Kamis (Seri: Hati Seorang Wanita)</button>
        <button class="tab-btn" onclick="filterTable('jumat', this)">Jumat (Seri: Baiti Jannati)</button>
    </div>

    <div class="table-container">
        <table id="scheduleTable">
            <thead>
                <tr>
                    <th>Hari & Tanggal</th>
                    <th>Jam Upload</th>
                    <th>Group List / Playlist</th>
                    <th>Part</th>
                    <th>Hook Cover (Slide 1)</th>
                    <th>Hashtag Booster</th>
                </tr>
            </thead>
            <tbody>
                <!-- Rabu -->
                <tr class="row-rabu">
                    <td><b>Rabu, 12 Agu 2026</b></td>
                    <td><span class="time-badge">13.00 WIB</span></td>
                    <td><span class="playlist-badge">Ciri Wanita Ahli Surga</span></td>
                    <td>Part 1/5</td>
                    <td>Untukmu wanita yang lelah, ini janji peleram gelisahmu...</td>
                    <td class="hashtag">#WanitaSholehah #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-rabu">
                    <td><b>Rabu, 12 Agu 2026</b></td>
                    <td><span class="time-badge">13.00 WIB</span></td>
                    <td><span class="playlist-badge">Ciri Wanita Ahli Surga</span></td>
                    <td>Part 2/5</td>
                    <td>Sifat kecil yang membuat pintu surga terbuka lebar...</td>
                    <td class="hashtag">#WanitaSholehah #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-rabu">
                    <td><b>Rabu, 12 Agu 2026</b></td>
                    <td><span class="time-badge">16.30 WIB</span></td>
                    <td><span class="playlist-badge">Ciri Wanita Ahli Surga</span></td>
                    <td>Part 3/5</td>
                    <td>Saat suami/keluarga lelah, dirimu jadi penenangnya...</td>
                    <td class="hashtag">#WanitaSholehah #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-rabu">
                    <td><b>Rabu, 12 Agu 2026</b></td>
                    <td><span class="time-badge">19.00 WIB</span></td>
                    <td><span class="playlist-badge">Ciri Wanita Ahli Surga</span></td>
                    <td>Part 4/5</td>
                    <td>Lisan yang teduh adalah perhiasan batin sesungguhnya...</td>
                    <td class="hashtag">#WanitaSholehah #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-rabu">
                    <td><b>Rabu, 12 Agu 2026</b></td>
                    <td><span class="time-badge">20.00 WIB</span></td>
                    <td><span class="playlist-badge">Ciri Wanita Ahli Surga</span></td>
                    <td>Part 5/5</td>
                    <td>Puncak ketenangan saat batin pasrah fully...</td>
                    <td class="hashtag">#WanitaSholehah #PenatHati #AmalanLangit</td>
                </tr>

                <!-- Kamis -->
                <tr class="row-kamis">
                    <td><b>Kamis, 13 Agu 2026</b></td>
                    <td><span class="time-badge">13.00 WIB</span></td>
                    <td><span class="playlist-badge">Seri: Hati Seorang Wanita</span></td>
                    <td>Part 1/5</td>
                    <td>Untuk kamu yang hatinya sering merasa sangat lelah...</td>
                    <td class="hashtag">#RuangJiwa #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-kamis">
                    <td><b>Kamis, 13 Agu 2026</b></td>
                    <td><span class="time-badge">13.00 WIB</span></td>
                    <td><span class="playlist-badge">Seri: Hati Seorang Wanita</span></td>
                    <td>Part 2/5</td>
                    <td>Simak nomor 2... Rahasia sabar yang tak terlihat mata.</td>
                    <td class="hashtag">#RuangJiwa #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-kamis">
                    <td><b>Kamis, 13 Agu 2026</b></td>
                    <td><span class="time-badge">16.30 WIB</span></td>
                    <td><span class="playlist-badge">Seri: Hati Seorang Wanita</span></td>
                    <td>Part 3/5</td>
                    <td>Bukan lemah, tapi caramu mengadu pada-Nya...</td>
                    <td class="hashtag">#RuangJiwa #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-kamis">
                    <td><b>Kamis, 13 Agu 2026</b></td>
                    <td><span class="time-badge">19.00 WIB</span></td>
                    <td><span class="playlist-badge">Seri: Hati Seorang Wanita</span></td>
                    <td>Part 4/5</td>
                    <td>Melepaskan beban dendam demi kedamaian jiwa...</td>
                    <td class="hashtag">#RuangJiwa #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-kamis">
                    <td><b>Kamis, 13 Agu 2026</b></td>
                    <td><span class="time-badge">20.00 WIB</span></td>
                    <td><span class="playlist-badge">Seri: Hati Seorang Wanita</span></td>
                    <td>Part 5/5</td>
                    <td>Kesabaranmu hari ini adalah mahkotamu kelak...</td>
                    <td class="hashtag">#RuangJiwa #PenatHati #AmalanLangit</td>
                </tr>

                <!-- Jumat -->
                <tr class="row-jumat">
                    <td><b>Jumat, 14 Agu 2026</b></td>
                    <td><span class="time-badge">13.00 WIB</span></td>
                    <td><span class="playlist-badge">Seri: Baiti Jannati</span></td>
                    <td>Part 1/5</td>
                    <td>Bukan tentang mewahnya, tapi indahnya kedamaian...</td>
                    <td class="hashtag">#RumahTeduh #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-jumat">
                    <td><b>Jumat, 14 Agu 2026</b></td>
                    <td><span class="time-badge">13.00 WIB</span></td>
                    <td><span class="playlist-badge">Seri: Baiti Jannati</span></td>
                    <td>Part 2/5</td>
                    <td>Doamu adalah benteng penyelamat keluarga...</td>
                    <td class="hashtag">#RumahTeduh #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-jumat">
                    <td><b>Jumat, 14 Agu 2026</b></td>
                    <td><span class="time-badge">16.30 WIB</span></td>
                    <td><span class="playlist-badge">Seri: Baiti Jannati</span></td>
                    <td>Part 3/5</td>
                    <td>Saat pintu rumah dibuka, hilangkan semua penat...</td>
                    <td class="hashtag">#RumahTeduh #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-jumat">
                    <td><b>Jumat, 14 Agu 2026</b></td>
                    <td><span class="time-badge">19.00 WIB</span></td>
                    <td><span class="playlist-badge">Seri: Baiti Jannati</span></td>
                    <td>Part 4/5</td>
                    <td>Trik kecil Rasulullah menjaga kehangatan rumah...</td>
                    <td class="hashtag">#RumahTeduh #PenatHati #AmalanLangit</td>
                </tr>
                <tr class="row-jumat">
                    <td><b>Jumat, 14 Agu 2026</b></td>
                    <td><span class="time-badge">20.00 WIB</span></td>
                    <td><span class="playlist-badge">Seri: Baiti Jannati</span></td>
                    <td>Part 5/5</td>
                    <td>Semoga rumah kita menjadi kumpulannya kelak di surga...</td>
                    <td class="hashtag">#RumahTeduh #PenatHati #AmalanLangit</td>
                </tr>
            </tbody>
        </table>
    </div>

    <script>
        function filterTable(day, btn) {
            let rows = document.querySelectorAll('#scheduleTable tbody tr');
            let tabs = document.querySelectorAll('.tab-btn');
            
            tabs.forEach(t => t.classList.remove('active'));
            btn.classList.add('active');

            rows.forEach(row => {
                if (day === 'all') {
                    row.style.display = '';
                } else {
                    if (row.classList.contains('row-' + day)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
        }

        function downloadCSV() {
            let csv = 'Hari & Tanggal,Jam Upload,Group List,Part,Hook,Hashtags\\n';
            let rows = document.querySelectorAll('#scheduleTable tbody tr');
            
            rows.forEach(row => {
                let cols = row.querySelectorAll('td');
                let rowData = [];
                cols.forEach(col => {
                    rowData.push('"' + col.innerText.replace(/\\n/g, ' ') + '"');
                });
                csv += rowData.join(',') + '\\n';
            });

            let blob = new Blob([csv], { type: 'text/csv' });
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.setAttribute('href', url);
            a.setAttribute('download', 'Jadwal_Gebrakan_Emas_RuangTeduh.csv');
            a.click();
        }
    </script>
</body>
</html>
"""

# Render HTML di Streamlit
components.html(html_code, height=850, scrolling=True)
