import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.HashMap;

import org.opencv.core.*;
import org.opencv.core.Core.*;
//import org.opencv.features2d.FeatureDetector;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.*;
import org.opencv.objdetect.*;

public class MapTestRead {

    public static void main(String[] args) throws FileNotFoundException {
        Mat mapx = new Mat(720, 1280, CvType.CV_64FC1);
        Mat mapy = new Mat(720, 1280, CvType.CV_64FC1);


        Scanner in = new Scanner(new File("mapx_values.csv"));
        in.useDelimiter(",");
        for(int row= 0; row <720; row++){
            for(int col = 0; col < 1280; col++ ){
                float num = in.nextFloat();
                mapx.put(row, col, num);
            }
        }

        in = new Scanner(new File("mapy_values.csv"));
        in.useDelimiter(",");
        for(int row= 0; row <720; row++){
            for(int col = 0; col < 1280; col++ ){
                float num = in.nextFloat();
                mapy.put(row, col, num);
            }
        }

        System.out.println("map x: "+mapx.toString());
        System.out.println("map y: "+mapy.toString());


    }
}
