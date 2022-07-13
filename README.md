# Persephone
Predict Air Quality (pm 2.5) over LA county using limited sensor data and open street map data.

> Note: You'll need tslearn to run my code. I have added a
> requirements.txt file. You can get the required libraries using pip
> install -r requirements.txt.

1.  The number of clusters and the cluster label for each sensor
    location

Number of clusters - 4

{1128: 3, 132561: 0, 1650: 0, 1852: 0, 2504: 1, 2749: 2, 3487: 2, 5222:
0, 6164: 2, 6472: 2, 6836: 1, 9076: 0, 9108: 1, 9168: 0, 17583: 0,
23263: 0, 23295: 0, 23347: 0, 27109: 2, 27113: 0, 28457: 1, 28515: 2,
28973: 0, 29295: 0, 30737: 0, 32339: 0, 33235: 1, 33855: 0, 34517: 2,
34519: 2, 35027: 2, 37193: 1, 37217: 0, 38399: 0, 39155: 0, 40639: 0,
42251: 2, 42857: 0, 52071: 1, 53825: 0, 54977: 0, 54981: 1, 54985: 1,
54993: 0, 55251: 0, 55351: 2, 56073: 2, 56141: 2, 63387: 2, 69201: 2,
71813: 2, 72459: 0, 74069: 0, 75839: 0, 76465: 1, 76469: 2, 76473: 2,
76627: 0, 76867: 2, 77427: 2, 78587: 0, 80069: 2, 80657: 1, 80807: 2,
81219: 2, 81363: 2, 81851: 2, 82271: 0, 83041: 2, 83081: 2, 83647: 2,
83895: 2, 84069: 2, 84083: 2, 84489: 2, 85253: 2, 85359: 2, 85373: 2,
85829: 2, 85985: 2, 86185: 0, 86367: 2, 86951: 0, 87315: 0, 87323: 2,
87413: 0, 87415: 2, 88895: 2, 90005: 0, 94397: 0, 96487: 2, 96793: 1,
99139: 2, 102032: 2, 104892: 2, 104900: 0, 104940: 1, 108518: 0, 110602:
0, 6228: 1, 6244: 1, 6886: 1, 14859: 2, 22675: 0, 34495: 0, 36143: 2,
36717: 0, 37885: 0, 40449: 2, 40721: 1, 40725: 1, 51323: 0, 52277: 1,
53043: 0, 61565: 0, 70793: 0, 78637: 1, 81379: 0, 84101: 2, 87129: 0,
87477: 1, 87567: 2, 90819: 1, 96243: 0, 102064: 0, 107960: 0}

2.  The total number of features in the geographic abstraction vector

5854

3.  The top 20 important features and their importance 

![Screenshot 2022-07-13 at 11 04 54 AM](https://user-images.githubusercontent.com/35135771/178779912-644a16d8-6ee9-4af5-b50f-f255b576cba9.png)

4.  Overall MSE and R2 on test samples and the plot showing hourly MSE
    and R2 scores 

Hourly R2 Score:

![image](https://user-images.githubusercontent.com/35135771/178602161-372b1dc1-88f1-411e-8e6c-b34fd08c1da1.png)


Hourly MSE Score:

![image](https://user-images.githubusercontent.com/35135771/178602187-6c3601a8-1db6-4ef2-9259-b2dd596f305a.png)

R2 Score for the entire dataset: 0.6164421802520904

Mean Squared Error Score for the entire dataset: 146.37517723504774

5\. Four plots of fine-grained prediction results (screen shots) 

Plot of 6 am to 9 am:

![image](https://user-images.githubusercontent.com/35135771/178602233-e86744c0-af63-4b3d-9e52-f495f14e229f.png)

Plot of 4 pm to 7pm:

![image](https://user-images.githubusercontent.com/35135771/178602293-e88ddc46-f591-4273-afa2-bb1cefff4b67.png)

Plot of weekdays:

![image](https://user-images.githubusercontent.com/35135771/178602314-1e937251-9098-4ff1-a5a1-77a96a24003f.png)

Plot of weekends:

![image](https://user-images.githubusercontent.com/35135771/178602349-108e770f-d5ed-47b1-9daf-9005ca76cb0e.png)

6\. Findings and discussion on the selected features, MSE and R2
scores, and plots of finegrained predictions in several sentences
Selected features:

I have selected the top 60 features based on the importance scores. They
intuitively make a lot of sense because highway occurs quite often in
those features. 25 out of the 60 features have highway. So does building
which occurs in 18 out of the 60 features. Waterway occurs in 6 of those
features. Highway and building will negatively impact the pm2.5
concentration whereas waterway will have the opposite effect.

MSE and R2 scores:

The overall MSE and R2 scores are good and show that the model did learn
something and was able to make decently accurate predictions. The R2
scores peak during the daytime. I think that can be attributed to lower
variability in pm2.5 scores as opposed to the nighttime.

Plots of fine-grained predictions:

It is clearly visible that pm2.5 concentrations are shown to be higher
along the roads especially when the roads are not surrounded by
vegetation. This is beautifully illustrated in the La Puento area where
the pollution concentration takes the shape of the curved road. The area
around Malibu always has lower concentration of pollution primarily
because of abundance of waterway and vegetation. Roads that directly
lead to downtown always have higher concentration when compared to other
roads. Weekdays have higher concetration of pm2.5 around the downtown
area compared to weekends. The area near vegetation has really low
levels of pm2.5.

Appendix:

Number of clusters vs Inertia

![image](https://user-images.githubusercontent.com/35135771/178602397-1956ead8-dd7d-4082-8457-0edc42bfe876.png)

TimeSeries Clusters:

![image](https://user-images.githubusercontent.com/35135771/178602411-2231bfa8-77f5-465e-9096-8e56797029e1.png)

![image](https://user-images.githubusercontent.com/35135771/178602438-48b46a90-3ac6-4acf-a9d5-d82b6bb86989.png)
