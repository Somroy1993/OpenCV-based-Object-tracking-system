import cv2
import numpy as np
import os
import csv


class CarTracking:
    def __init__(self, path_to_dataset='tracking-data'):
        self.path = path_to_dataset
        if not os.path.exists('output'):
            os.makedirs('output')
        self.settings = {
            'fps': 30,
            'max_contour_area': 6500,
            'min_contour_area': 1000,
            'max_aspect_ratio': 3.5,
            'min_aspect_ratio': 1.5
        }

    def tracking(self):
        files = sorted(os.listdir(self.path))
        out_video_path = os.path.join('output', str(self.settings['fps']) + 'fps_output_video.avi')
        out_csv_path = os.path.join('output', str(self.settings['fps']) + 'fps_output_csv.csv')
        video = cv2.VideoWriter(out_video_path, 0, self.settings['fps'], (1280, 720))
        frame_coordinates = []

        for i in range(len(files) - 1):
            if files[i].endswith('.jpg'):
                if i == 0: frame1 = cv2.imread(os.path.join(self.path, files[i]))
                frame2 = cv2.imread(os.path.join(self.path, files[i + 1]))
                frame, contour_coordinates = self.plot_contours(frame1, frame2)
                temp = {'frame_name': files[i], 'coordinates': contour_coordinates}
                frame_coordinates.append(temp)
                # Appending the images to the video one by one
                video.write(frame)
                frame1 = frame2

        cv2.destroyAllWindows()
        video.release()
        with open(out_csv_path, mode='w') as csv_file:
            fieldnames = ['frame_name', 'coordinates']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for data in frame_coordinates:
                writer.writerow(data)

    def plot_contours(self, frame1, frame2):
        d = cv2.absdiff(frame1, frame2)
        grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (5, 5), 0)
        ret, th = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)
        thresh_gray = cv2.morphologyEx(th, cv2.MORPH_CLOSE,
                                       cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51, 51)))
        # cv2.imshow('thresh gray', thresh_gray)
        # cv2.waitKey(0)
        contours, hierarchy = cv2.findContours(thresh_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = np.array(contours, dtype=object)
        filtered_contours, contours_coordinate = self.filter_contours(contours)
        count = 0
        for contour in filtered_contours:
            (x, y, w, h) = contour
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame1, str(count), (x, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(255, 0, 0), thickness=2)
            count += 1
        # frame1 = cv2.drawContours(frame1, c, -1, (0, 0, 255), 3)
        # cv2.imshow("Original", frame2)
        # cv2.imshow("Output", frame1)
        # cv2.waitKey(0)
        # if cv2.waitKey(0) == 27:  # exit on ESC
        #     sys.exit()
        cv2.destroyAllWindows()
        return frame1, contours_coordinate

    def filter_contours(self, contours):
        filtered_contours = []
        contours_coordinate = []
        count = 0
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            aspect_ratio = w / h
            if (self.settings.get('max_contour_area') > cv2.contourArea(contour) > self.settings.get('min_contour_area')) and (aspect_ratio > self.settings.get('min_aspect_ratio')) and (x > 0) and (y > 0):
                temp = {'contour_' + str(count): (x, y, w, h)}
                contours_coordinate.append(temp)
                print('parameters for contour no: ' + str(count))
                print('area', cv2.contourArea(contour))
                print('aspect_ratio:', aspect_ratio)
                print((x, y, w, h))
                filtered_contours.append((x, y, w, h))
                count += 1
        print('fc', len(filtered_contours))
        return filtered_contours, contours_coordinate


if __name__ == "__main__":
    CT = CarTracking()
    CT.tracking()
