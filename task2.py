import argparse
import pickle
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score,mean_squared_error
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


def main():
    important_features = pickle.load( open( "important_features.p", "rb" ) )
    important_features = important_features[:60]
    feature_vector = pd.read_csv('generated_stuff_all.csv')
    feature_vector = feature_vector.set_index('sensor_id')
    feature_vector_important = feature_vector[important_features]
    timeseries = pd.read_csv(args.sensor_obs)
    timeseries = timeseries.set_index('sensor_id')
    mega_dataframe = timeseries.join(feature_vector_important)
    column_names = important_features + ['timestamp','pm2.5']
    time_unique = mega_dataframe.timestamp.unique()
    mega_dataframe = mega_dataframe.reindex(columns=column_names)
    mega_dataframe['timestamp'] = pd.to_datetime(mega_dataframe['timestamp'])
    grouped = mega_dataframe.groupby('timestamp')

    mega_dataframe_timegrouped = []

    for i in range(len(time_unique)):
        mega_dataframe_timegrouped.append(grouped.get_group(time_unique[i]))
    for i in range(len(mega_dataframe_timegrouped)):
        mega_dataframe_timegrouped[i] = mega_dataframe_timegrouped[i].drop(columns=['timestamp'])
        mega_dataframe_timegrouped[i] = mega_dataframe_timegrouped[i].fillna(0)
    X_grouped = []
    for i in range(len(mega_dataframe_timegrouped)):
        X_grouped.append(mega_dataframe_timegrouped[i].iloc[: , :-1])
    y_grouped = []
    for i in range(len(mega_dataframe_timegrouped)):
        y_grouped.append(mega_dataframe_timegrouped[i].iloc[: , -1:])
    clf_grouped = []
    for i in range(len(mega_dataframe_timegrouped)):
        clf_grouped.append(RandomForestRegressor(random_state=0))

    for i in range(len(mega_dataframe_timegrouped)):
        clf_grouped[i].fit(X_grouped[i],y_grouped[i])

    with open('classifiers_galore.pickle', 'wb') as handle:
        pickle.dump(clf_grouped, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(args.model_path, 'wb') as handle:
        pickle.dump(clf_grouped, handle, protocol=pickle.HIGHEST_PROTOCOL)


    timeseries_test = pd.read_csv('data/county_sensor_observations_test.csv')
    timeseries_test = timeseries_test.set_index('sensor_id')
    mega_dataframe_test = timeseries_test.join(feature_vector_important)
    column_names = important_features + ['timestamp','pm2.5']
    mega_dataframe_test = mega_dataframe_test.reindex(columns=column_names)
    mega_dataframe_test['timestamp'] = pd.to_datetime(mega_dataframe_test['timestamp'])
    grouped_test = mega_dataframe_test.groupby('timestamp')
    mega_dataframe_timegrouped_test = []
    for i in range(len(time_unique)):
        mega_dataframe_timegrouped_test.append(grouped_test.get_group(time_unique[i]))

    for i in range(len(mega_dataframe_timegrouped)):
        mega_dataframe_timegrouped_test[i] = mega_dataframe_timegrouped_test[i].drop(columns=['timestamp'])
        mega_dataframe_timegrouped_test[i] = mega_dataframe_timegrouped_test[i].fillna(0)

    X_grouped = []
    for i in range(len(mega_dataframe_timegrouped_test)):
        X_grouped.append(mega_dataframe_timegrouped_test[i].iloc[: , :-1])

    y_grouped_pred = []
    for i in range(len(mega_dataframe_timegrouped_test)):
        y_grouped_pred.append(clf_grouped[i].predict(X_grouped[i]))

    predictions_data = []
    for i in range(len(y_grouped_pred)):
        for j in range(len(X_grouped[0])):
            predictions_data.append([X_grouped[0].index[j],mega_dataframe_test['timestamp'].unique()[i],y_grouped_pred[i][j]])

    predictions_dataframe = pd.DataFrame(predictions_data,columns=['sensor_id','timestamp','prediction'])  
    predictions_dataframe = predictions_dataframe.set_index('sensor_id')
    predictions_dataframe.to_csv(args.prediction)

    y = []
    for i in range(len(mega_dataframe_timegrouped_test)):
        y.append(mega_dataframe_timegrouped_test[i].iloc[: , -1:])

    hourly_collection_bin_real = [[] for _ in range(24)]
    hourly_collection_bin_predict = [[] for _ in range(24)]
    for i in range(len(y)):
        for element in y[i]['pm2.5']:
            hourly_collection_bin_real[i%24].append(element)
        for element in y_grouped_pred[i]:
            hourly_collection_bin_predict[i%24].append(element)

    hourly_r2_score = []
    hourly_mean_squared_error = []
    for i in range(len(hourly_collection_bin_real)):
        #print(r2_score(hourly_collection_bin_real[i],hourly_collection_bin_predict[i]))
        hourly_r2_score.append(r2_score(hourly_collection_bin_real[i],hourly_collection_bin_predict[i]))
        #print(mean_squared_error(hourly_collection_bin_real[i],hourly_collection_bin_predict[i]))
        hourly_mean_squared_error.append(mean_squared_error(hourly_collection_bin_real[i],hourly_collection_bin_predict[i]))

    y_collect = []
    y_pred_collect = []
    for i in range(len(mega_dataframe_timegrouped_test)):
        for j in y[i]['pm2.5']:
            y_collect.append(j)
    for i in range(len(mega_dataframe_timegrouped_test)):
        for j in y_grouped_pred[i]:
            y_pred_collect.append(j)

    print("R2 Score for the entire dataset: " + str(r2_score(y_collect, y_pred_collect)) + "\n")
    print("Mean Squared Error Score for the entire dataset: " + str(mean_squared_error(y_collect, y_pred_collect)) + "\n")
    print("Hourly R2 Score:\n")
    print(hourly_r2_score)
    print("Hourly Mean Squared Error Score:\n")
    print(hourly_mean_squared_error)

    geo_features = pd.read_csv('data/county_grid_geographic_features.csv')
    geo_features = geo_features.set_index('grid_id')
    grids = pd.read_csv('data/county_grids.csv')
    grids = grids.set_index('grid_id')
    mega_dataframe = grids.join(geo_features)
    important_features = pickle.load( open( "important_features.p", "rb" ) )
    important_features = important_features[:60]

    master_feature_beakdown = []
    for i in range(len(important_features)):
        if(len(important_features[i].split('_'))==3):
            geo_feature = important_features[i].split('_')[0]
            feature_type = important_features[i].split('_')[1]
            buffer_size = important_features[i].split('_')[2]
        elif(len(important_features[i].split('_'))==4):
            geo_feature = important_features[i].split('_')[0]
            feature_type = important_features[i].split('_')[1]+'_'+important_features[i].split('_')[2]
            buffer_size = important_features[i].split('_')[3]
        else:
            print("This isn't good")
            exit()
        master_feature_beakdown.append([geo_feature,feature_type,buffer_size])
    
    df2 = pd.DataFrame(data=None, columns=mega_dataframe.columns)

    for feature_spec in master_feature_beakdown:
        df2 = df2.append(mega_dataframe.loc[(mega_dataframe['geo_feature'] == feature_spec[0]) & (mega_dataframe['feature_type'] == feature_spec[1]) & (mega_dataframe['buffer_size'] == int(feature_spec[2]))])

    df2 = df2.sort_index()
    features_numbers = pd.DataFrame(columns = important_features+['grid_id'])
    features_numbers = features_numbers.set_index('grid_id')

    for i, row in df2.iterrows():
        column_name = row['geo_feature']+'_'+row['feature_type']+'_'+str(row['buffer_size'])
        features_numbers.at[i, column_name] = row['value']
    features_numbers = features_numbers.fillna(0)

    feature_maxval_dict = pickle.load( open( "feature_maxval_dict.p", "rb" ) )
    
    for column in features_numbers:
        features_numbers[column] = features_numbers[column].div(float(feature_maxval_dict[column]))

    with open('classifiers_galore.pickle', 'rb') as handle:
        clf_grouped = pickle.load(handle)

    master_collector = []
    for j in clf_grouped:
        grid_id_collector = j.predict(features_numbers)
        master_collector.append(grid_id_collector)

    timeseries = pd.read_csv(args.sensor_obs)
    grid_id_result = []
    unique_timestamps = timeseries.timestamp.unique()
    features_numbers_index = features_numbers.index
    for i in range(len(unique_timestamps)):
        for j in range(len(master_collector[0])):
            grid_id_result.append([features_numbers_index[j],unique_timestamps[i],master_collector[i][j]])

    predictions_dataframe = pd.DataFrame(grid_id_result,columns=['grid_id','timestamp','prediction'])  
    predictions_dataframe.to_csv('grid_prediction.csv')



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