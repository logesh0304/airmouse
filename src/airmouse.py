import socket 
import pyautogui

HOST=""
PORT=8080
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
reader=conn=None
def startserver():
    global reader, conn
    server.bind((HOST, PORT))
    server.listen(1)
    print("Server started")
    print("address :" + socket.gethostbyname(socket.gethostname()))
    print("waiting for connection...")
    conn, addr = server.accept()
    print(f"connection from {addr}")
    reader=conn.makefile('rb', -1)

pyautogui.PAUSE=0
scr_width, scr_height = pyautogui.size()
x_half_dim = scr_width / 2
y_half_dim =/home/mandarin/Documents/airmouse/airmouse.py scr_height / 2
az_max_limit = 30
pi_max_limit = 30
print(f"screen resolution : {scr_width} x {scr_height}")

ref_az=0.0

# converts degrees value from sensor to coordinates of screen
# half_dim - half of dimension (width or height) of screen
def degtocoord(deg, max_limit, half_dim):
    # deg = max_limit if the deg is more than max_limit
    deg = deg if abs(deg) < max_limit else max_limit
    # coordinate with respect to screens center and origin
    coord_wrt_scr_center = (deg / max_limit) * half_dim
    coord_wrt_scr_origin = half_dim + coord_wrt_scr_center
    return coord_wrt_scr_origin

def getsensorvalues():
    global ref_az
    line=reader.readline()[:-2].decode()
    if not line :
        return 
    elif not line[0].isdigit():
        values=getsensorvalues()
        ref_az=values['azimuth']
        return values
    prox, d1, d2, az, pi, ro = map(float, line.split(','))
    return dict(proximity = not bool(int(prox)), azimuth=az, pitch=pi, roll=ro)

def localize_azimuth(azimuth):
    if azimuth > 270.0 and azimuth < 360.0:
        azimuth = azimuth - 360.0
    return azimuth

def close():
    conn.close()
    print("server closed")

if __name__=="__main__" :

    mouse_left_down = False
    startserver()
    while values:=getsensorvalues() :

        values['azimuth'] = localize_azimuth(values['azimuth'])-ref_az
        print(values)
        xpos = degtocoord(values['azimuth'], az_max_limit, x_half_dim)
        ypos = degtocoord(values['pitch'], pi_max_limit, y_half_dim)
        pyautogui.moveTo(xpos, ypos)

        if values['proximity'] and not mouse_left_down:
            pyautogui.mouseDown(button='left')
            mouse_left_down = True
        elif not values['proximity'] and mouse_left_down:
            pyautogui.mouseUp(button='left')
            mouse_left_down = False
    
    if mouse_left_down:
        pyautogui.mouseUp(button='left')

    close()