import qrcode
from PIL import Image
#from pyzbar.pyzbar import decode

def generate_qr_code(product_details):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(str(product_details))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    qr_code_path = f"qrcodes/product{product_details['uniqueid']}.png"
    img.save("static/"+qr_code_path)
    print(qr_code_path)
    return qr_code_path

def decode_qr_code(qr_code_image):
    img = Image.open(qr_code_image)
    decoded_objects = decode(img)
    
    if decoded_objects:
        # Extract and return the decoded information
        product_details = decoded_objects[0].data.decode("utf-8")
        return product_details
    else:
        return None
