import cv2
import argparse

def video_capture(trackingType):
    cap = cv2.VideoCapture(0)

    tracker = None

    while True:
        ret, frame = cap.read()

        if cv2.waitKey(1) & 0xFF == ord('c'):
            print("here?")
            tracker = tracking_init(frame, trackingType)

        if tracker != None:
            get_tracking_bounding_box(frame, tracker)

        cv2.imshow("Image", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def tracking_init(frame, tracker_id = "Moose"):
    bb = cv2.selectROI("Image", frame, False)

    object_trackers = {
        "csrt": cv2.TrackerCSRT_create,
        "kcf": cv2.TrackerKCF_create,
        "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        "tld": cv2.TrackerTLD_create,
        "medianflow": cv2.TrackerMedianFlow_create,
        "mosse": cv2.TrackerMOSSE_create
    }

    if tracker_id == "csrt":
        tracker = object_trackers["csrt"]()
    elif tracker_id == "kcf":
        tracker = object_trackers["kcf"]()
    elif tracker_id == "boosting":
        tracker = object_trackers["boosting"]()
    elif tracker_id == "mil":
        tracker = object_trackers["mil"]()
    elif tracker_id == "tld":
        tracker = object_trackers["tld"]()
    elif tracker_id == "medianflow":
        tracker = object_trackers["medianflow"]()
    elif tracker_id == "mosse":
        tracker = object_trackers["mosse"]()
    else:
        print("Did not find that tracker you wanted, default will be csrt")
        tracker = object_trackers["csrt"]()

    tracker.init(frame, bb)
    return tracker


def get_tracking_bounding_box(frame, tracker):
    tracker_ret, bbox = tracker.update(frame)

    if tracker_ret:
        x, y, w, h = bbox
        pt1 = (int(x), int(y))
        pt2 = (int(x + w), int(y + h))
        color = (255)

        cv2.rectangle(frame, pt1, pt2, color)

def display_models():
    object_trackers = ["csrt", "kcf", "boosting", "mil", "tld", "medianflow", "mosse"]
    print("All the Models That are in effect")
    for tracker in object_trackers:
        print(f"\t{tracker}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tracker', help='What Kind of Tracker Do You want to have (default csrt)', type=str)
    parser.add_argument('-m', '--models', help="What Models are currently there", default="false")
    args = parser.parse_args()

    if args.models.lower() == "true":
        display_models()
    else:
        video_capture(args.tracker)