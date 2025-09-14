import qrcode
import socket
import os

# Get your local IP address
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Build your Flask site URL
url =  " https://great-dodos-crash.loca.lt"

# Create QR code
qr = qrcode.make(url)

# Save to static folder
static_dir = "static"
os.makedirs(static_dir, exist_ok=True)
qr_path = os.path.join(static_dir, "healtho_qr.png")
qr.save(qr_path)

print(f"✅ QR code saved at {qr_path}")
print(f"📱 Scan this on your phone to access: {url}")
