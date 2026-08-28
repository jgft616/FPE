#!/usr/bin/env python3
"""
Platoboost Bypass Server
Flask backend that uses deltax to bypass ad-wall key systems.
"""

import sys
import os
import json
import traceback
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# Add current directory to path so deltax can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import deltax

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Supported platforms
SUPPORTED_PATTERNS = [
    'platorelay.com',
    'platoboost.com',
    'gateway.platoboost.com',
    'linkvertise.com',
    'lootlabs.gg',
    'loot-link.com',
    'loot-links.com',
    'lootlink.org',
    'lootlinks.co',
    'lootdest.info',
    'lootdest.org',
    'lootdest.com',
    'links-loot.com',
    'linksloot.net',
    'work.ink',
    'workink.com',
    'jnkie.com',
]


@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_file('index.html')


@app.route('/standalone')
def standalone():
    """Serve the standalone HTML page."""
    return send_file('standalone.html')


@app.route('/health')
def health():
    """Health check endpoint for Render."""
    return jsonify({'status': 'ok'}), 200


@app.route('/api/bypass', methods=['POST'])
def bypass():
    """
    Bypass an ad-wall link and return the key.
    
    Request body:
        { "url": "https://auth.platorelay.com/a?d=..." }
    
    Response:
        { "success": true, "key": "FREE_...", "timeLeft": "24小时0分钟" }
        or
        { "success": false, "message": "Error description" }
    """
    try:
        data = request.get_json(force=True)
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'success': False, 'message': '请输入链接地址'}), 400
        
        # Validate URL
        if not url.startswith('http'):
            url = 'https://' + url
        
        # Check if URL is supported
        is_supported = any(pattern in url for pattern in SUPPORTED_PATTERNS)
        if not is_supported:
            return jsonify({
                'success': False, 
                'message': f'不支持的链接类型。支持的平台: {", ".join(SUPPORTED_PATTERNS[:5])}...'
            }), 400
        
        print(f"[*] Bypassing: {url[:80]}...")
        
        # Determine service type
        service = None
        if 'linkvertise' in url or 'platorelay' in url or 'platoboost' in url:
            service = 1  # linkvertise
        elif 'loot' in url:
            service = 2  # lootlabs
        elif 'work.ink' in url or 'workink' in url:
            service = 4  # workink
        
        # Call deltax to bypass
        key = None
        error_msg = None
        
        try:
            if service:
                key = deltax.getKey(url, service=service)
            else:
                key = deltax.getKey(url)
        except Exception as e:
            error_msg = str(e)
            traceback.print_exc()
        
        if key and key != 'KEY_NOT_FOUND':
            # Try to get time left from PlatoRelay API
            time_left = None
            try:
                if 'platorelay.com' in url and '?d=' in url:
                    from urllib.parse import urlparse, parse_qs
                    parsed = urlparse(url)
                    params = parse_qs(parsed.query)
                    ticket = params.get('d', [None])[0]
                    if ticket:
                        import requests as req
                        status_url = f'https://auth.platorelay.com/api/session/status?ticket={ticket}'
                        resp = req.get(status_url, timeout=10)
                        status_data = resp.json()
                        if status_data.get('success') and status_data.get('data'):
                            minutes = status_data['data'].get('minutesLeft', 0)
                            if minutes > 0:
                                hours = minutes // 60
                                mins = minutes % 60
                                time_left = f'{hours}小时{mins}分钟'
            except Exception:
                pass
            
            result = {'success': True, 'key': key}
            if time_left:
                result['timeLeft'] = time_left
            
            print(f"[+] Success! Key: {key}")
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'message': error_msg or '绕过失败，密钥未找到。请检查链接是否正确或稍后重试。'
            }), 500
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Check server status."""
    return jsonify({
        'status': 'running',
        'version': deltax.__version__,
        'supported': SUPPORTED_PATTERNS
    })


@app.route('/api/bypass/status', methods=['GET'])
def bypass_status():
    """Check the status of a PlatoRelay ticket directly."""
    ticket = request.args.get('ticket', '')
    if not ticket:
        return jsonify({'success': False, 'message': 'Missing ticket parameter'}), 400
    
    try:
        import requests as req
        status_url = f'https://auth.platorelay.com/api/session/status?ticket={ticket}'
        resp = req.get(status_url, timeout=10, 
                       headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("  Platoboost Bypass Server")
    print(f"  deltax v{deltax.__version__}")
    print("=" * 50)
    print("  Server: http://localhost:5000")
    print("  API:    http://localhost:5000/api/bypass")
    print("=" * 50)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
