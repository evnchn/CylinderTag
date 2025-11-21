#include "header/CylinderTag.h"

using namespace std;
using namespace cv;

Mat frame, img_gray;
vector<MarkerInfo> markers;
vector<ModelInfo> marker_model;
CamInfo camera;
vector<PoseInfo> pose;

void read_from_image(const string& path, const string& marker_path, const string& model_path, const string& camera_path, const string& output_path);
void read_from_video(const string& path);

int main(int argc, char** argv){
	google::InitGoogleLogging(argv[0]);
	
	string image_path = "../test.bmp";
	string marker_path = "../CTag_2f12c.marker";
	string model_path = "../CTag_2f12c.model";
	string camera_path = "../cameraParams.yml";
	string output_path = "../output.bmp";

	if(argc > 1) image_path = argv[1];
	if(argc > 2) marker_path = argv[2];
	if(argc > 3) model_path = argv[3];
	if(argc > 4) camera_path = argv[4];
	if(argc > 5) output_path = argv[5];
	
	read_from_image(image_path, marker_path, model_path, camera_path, output_path);
	//read_from_video("../test.avi"); 

	//waitKey(0);
	//destroyAllWindows();
	//system("Pause");

	return 0;
}

void read_from_image(const string& path, const string& marker_path, const string& model_path, const string& camera_path, const string& output_path){
	frame = imread(path);

	CylinderTag marker(marker_path);
	marker.loadModel(model_path, marker_model);
	marker.loadCamera(camera_path, camera);

	if (frame.channels() == 3) {
		cvtColor(frame, img_gray, COLOR_BGR2GRAY);
	}

	marker.detect(img_gray, markers, 5, true, 5);
	marker.estimatePose(img_gray, markers, marker_model, camera, pose, false);
	cout << "========== RAW POSE DATA OUTPUT ==========" << endl;
	cout << "Number of markers detected: " << pose.size() << endl << endl;
	for (size_t i = 0; i < pose.size(); ++i) {
		cout << "Marker ID: " << pose[i].markerID << endl;
		cout << "Rotation Vector (rvec):" << endl;
		cout << "[" << pose[i].rvec.at<double>(0, 0) << ";" << endl;
		cout << " " << pose[i].rvec.at<double>(1, 0) << ";" << endl;
		cout << " " << pose[i].rvec.at<double>(2, 0) << "]" << endl;
		cout << "Translation Vector (tvec):" << endl;
		cout << "[" << pose[i].tvec.at<double>(0, 0) << ";" << endl;
		cout << " " << pose[i].tvec.at<double>(1, 0) << ";" << endl;
		cout << " " << pose[i].tvec.at<double>(2, 0) << "]" << endl << endl;
	}
	marker.drawAxis(img_gray, markers, marker_model, pose, camera, 30, output_path);
}

void read_from_video(const string& path){
	VideoCapture capture; 
	frame = capture.open(path );	

	CylinderTag marker("../CTag_2f12c.marker");
	marker.loadModel("../CTag_2f12c.model", marker_model);
	marker.loadCamera("../cameraParams.yml", camera);

	while (capture.read(frame))
	{	
		cvtColor(frame, img_gray, COLOR_BGR2GRAY);
		markers.clear();
		pose.clear();
		marker.detect(img_gray, markers, 5, true, 5);
		marker.estimatePose(img_gray, markers, marker_model, camera, pose, false);
		marker.drawAxis(img_gray, markers, marker_model, pose, camera, 30, "output.png");
	}
}
