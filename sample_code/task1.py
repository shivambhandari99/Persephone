import argparse


def main():
    pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--sensor_loc', type=str, default='data/county_sensor_locations_train.csv',
                        help='The file to the locations (train).')
    parser.add_argument('--sensor_obs', type=str, default='data/county_sensor_observations_train.csv',
                        help='The file to the sensor observations (train).')
    parser.add_argument('--sensor_geo', type=str, default='data/county_sensor_geographic_features.csv',
                        help='The file to the sensor geographic features.')
    parser.add_argument('--model_path', type=str, default='data/model.save',
                        help='The file to save the model.')
    args = parser.parse_args()

    main()
