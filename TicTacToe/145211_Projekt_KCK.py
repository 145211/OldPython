import numpy as np
import cv2


def main(img):
    gamestate = [["-", "-", "-"],
                 ["-", "-", "-"],
                 ["-", "-", "-"]]

    kernel = np.ones((7, 7), np.uint8)

    img_width = img.shape[0]
    img_height = img.shape[1]

    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(img_g, 100, 255, cv2.THRESH_BINARY)

    thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)

    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < 5:
        return 0

    contours = list(contours)
    contours.pop(0)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

    field_rect = cv2.boundingRect(contours[0])
    field_w = field_rect[2] - field_rect[0]
    field_h = field_rect[3] - field_rect[1]
    field_p = field_w * field_h
    tile_min_p = field_p/10

    tile_w = round(field_w/3)
    tile_h = round(field_h/3)
    contours.pop(0)

    trim = 0
    tile_count = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > (tile_min_p * 0.9):
            tile_count = tile_count + 1

            if tile_count > 9:
                break

            x, y, w, h = cv2.boundingRect(cnt)

            dist = round(0.1 * tile_w)
            tile = thresh1[(y + dist):(y + h - dist), (x + dist):(x + w - dist)]
            img_tile = img[(y + dist):(y + h - dist), (x + dist):(x + w - dist)]

            # a = [x + dist, y + dist]
            # b = [x + w - dist, y + h - dist]
            #
            # cv2.rectangle(img, a, b, (255, 0, 0), 2)

            c, hierarchy = cv2.findContours(tile, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for ct in c:
                if (cv2.contourArea(ct) < (tile_min_p * 0.9)) and (cv2.contourArea(ct) > (tile_min_p * 0.05)):
                    cv2.drawContours(img_tile, [ct], -1, (255, 0, 0), 2)

                    area = cv2.contourArea(ct)
                    hull = cv2.convexHull(ct)
                    hull_area = cv2.contourArea(hull)
                    if hull_area != 0:
                        solidity = float(area) / hull_area

                        if solidity > 0.7:
                            gamestate[(tile_count - 1)//3][(tile_count - 1) % 3] = "O"
                        else:
                            gamestate[(tile_count - 1)//3][(tile_count - 1) % 3] = "X"
                        break

            cv2.putText(img, str(tile_count), (x + dist, y + tile_h - dist), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    for line in gamestate:
        linetxt = ""
        for cel in line:
            linetxt = linetxt + "|" + cel
        print(linetxt + "|")

    res = cv2.resize(img, None, fx=(500 / img_width), fy=(500 / img_height), interpolation=cv2.INTER_CUBIC)

    cv2.imshow('tic_tac_toe', res)


video = 0

if __name__ == "__main__":
    if video:
        vid = cv2.VideoCapture(0)

        while True:
            success, frame = vid.read()
            main(frame)
            cv2.waitKey(100)

    else:
        imgs = ['game1.jpg', 'game2.jpg', 'game3.jpg', 'map.jpg']

        img = cv2.imread(imgs[1])

        main(img)
        cv2.waitKey(0)
