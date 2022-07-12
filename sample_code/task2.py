import argparse


def main():
    pass
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--sensor_loc', type=str, default='data/county_sensor_locations_train.csv',
                        help='The file to the sensor locations (train).')
    parser.add_argument('--sensor_obs', type=str, default='data/county_sensor_observations_train.csv',
                        help='The file to the sensor observations (train).')
    parser.add_argument('--sensor_geo', type=str, default='data/county_sensor_geographic_features.csv',
                        help='The file to the sensor geographic features.')
    parser.add_argument('--model_path', type=str, default='data/model.save',
                        help='The file of the model.')
    parser.add_argument('--target_loc', type=str, default='data/county_sensor_locations_test.csv',
                        help='The file to the target locations (test or grid).')
    parser.add_argument('--target_geo', type=str, default='data/county_sensor_geographic_features.csv',
                        help='The file to the geographic features of target locations (sensor or grid).')
    parser.add_argument('--prediction', type=str, default='data/test_prediction.csv',
                        help='The file to save the predictions.')

    args = parser.parse_args()

    main()