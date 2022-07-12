import argparse
import time
import pickle
import pandas as pd
import numpy as np
from tslearn.generators import random_walks
from tslearn.utils import to_time_series_dataset
from tslearn.clustering import TimeSeriesKMeans
import numpy
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tslearn.datasets import CachedDatasets
from tslearn.preprocessing import TimeSeriesScalerMeanVariance, \
    TimeSeriesResampler
from sklearn.ensemble import RandomForestClassifier

def generate_clusters():
    timeseries = pd.read_csv(args.sensor_obs)
    sensors = timeseries.sensor_id.unique()
    master_list = []
    for sensor in sensors:
        x = timeseries.loc[timeseries['sensor_id'] == sensor]
        master_list.append(x['pm2.5'].to_numpy().tolist())
    X_bis = to_time_series_dataset(master_list)


    seed = 0
    numpy.random.seed(seed)

    clusters = 4
    X_train = X_bis
    sz = X_train.shape[1]
    dba_km = TimeSeriesKMeans(n_clusters=clusters,
                                  n_init=1,
                                  metric="dtw",
                                  n_jobs=3,
                                  verbose=True,
                                  max_iter_barycenter=10,
                                  random_state=seed)
    print("DBA k-means")
    y_pred = dba_km.fit_predict(X_train)
        
    for yi in range(clusters):
        for xx in X_train[y_pred == yi]:
            plt.plot(xx.ravel(), "k-", alpha=.2)
        plt.plot(dba_km.cluster_centers_[yi].ravel(), "r-")
        plt.xlim(0, sz)
        plt.ylim(0, 180)
        plt.text(0.55, 0.85,'Cluster %d' % (yi + 1),
                 transform=plt.gca().transAxes)
        if yi == 1:
            plt.title("DBA $k$-means")
        #plt.show()

    for yi in range(clusters):
        plt.plot(dba_km.cluster_centers_[yi].ravel())
    #plt.show()
    dba_km.to_pickle(args.model_path)



    timeseries_test = pd.read_csv('data/county_sensor_observations_test.csv')
    sensors_test = timeseries_test.sensor_id.unique()
    master_list = []
    for sensor in sensors_test:
        x = timeseries_test.loc[timeseries_test['sensor_id'] == sensor]
        master_list.append(x['pm2.5'].to_numpy().tolist())
    X_bis = to_time_series_dataset(master_list)

    X_test = X_bis
    y_pred_test = dba_km.predict(X_test)
    return sensors,sensors_test,y_pred, y_pred_test


def main():
    
    f = open(args.sensor_geo,'r')
    columns_master = []
    for line in f:
        contents = line.split(',')
        column_name = contents[3]+'_'+contents[4]+'_'+contents[5]
        columns_master.append(column_name)
    columns_master = sorted(list(set(columns_master)))


    f = open(args.sensor_geo,'r')

    previous_sensor_id = "0"
    collector_of_results = []
    first_row = columns_master
    first_row.insert(0,'sensor_id')

    row = []
    for line in f:
        contents = line.split(',')
        column_name = contents[3]+'_'+contents[4]+'_'+contents[5]
        sensor_id = contents[1]
        if(sensor_id!=previous_sensor_id):
            previous_sensor_id = sensor_id
            collector_of_results.append(row)
            row = ["0" for i in range(len(columns_master))]
            row[0] = sensor_id
            row[first_row.index(column_name)] = contents[6].split('\n')[0]
        else:
            row[first_row.index(column_name)] = contents[6].split('\n')[0]
    del collector_of_results[0]
    del collector_of_results[0]

    df = pd.DataFrame(collector_of_results, columns = first_row)
    df = df.set_index('sensor_id')
    df = df.groupby('sensor_id').sum()
    sensors,sensors_test,y_pred, y_pred_test = generate_clusters()


    df_side = df.copy()

    min_max_scaler = MinMaxScaler()
    df[columns_master[1:]] = min_max_scaler.fit_transform(df[columns_master[1:]])
    df2 = pd.DataFrame(df, columns = columns_master[1:])

    sensor_cluster_dict = {}
    for i in range(len(sensors)):
        sensor_cluster_dict[sensors[i]] = y_pred[i]
    for i in range(len(sensors_test)):
        sensor_cluster_dict[sensors_test[i]] = y_pred_test[i]

    df3 = pd.DataFrame.from_dict(sensor_cluster_dict, orient='index')
    df3.index.name = 'sensor_id'
    df3 = df3.rename(columns={0: "cluster"})
    df3.to_csv('cluster_assignment.csv')
    df2.index = df2.index.astype(np.int64)
    df4 = df2.join(df3)
    X  = df4.iloc[: , :-1]
    y = df4.iloc[: , -1:]
    df4.to_csv('generated_stuff_all.csv')

    clf = RandomForestClassifier(random_state=0)
    clf.fit(X, y)

    features_cache = list(df4.columns[:-1])
    feature_importance_dict = {}
    for i in range(len(clf.feature_importances_)):
        feature_importance_dict[features_cache[i]] = clf.feature_importances_[i]

    result_importance = {k: v for k, v in sorted(feature_importance_dict.items(), key=lambda item: item[1],reverse=True)}
    
    important_features = []
    for i in range(len(list(result_importance.items())[:585])):
        important_features.append(list(result_importance.items())[:585][i][0])

    df_side = df_side.astype(float)
    feature_maxval_dict = {}
    for feature in important_features:
        column = df_side[feature]
        max_value = float(column.max())
        feature_maxval_dict[feature] = max_value

    pickle.dump( feature_maxval_dict, open( "feature_maxval_dict.p", "wb" ) )
    pickle.dump( important_features, open( "important_features.p", "wb" ) )

    important_features = pickle.load( open( "important_features.p", "rb" ) )

    importance_csv_collector = []
    for key in list(result_importance.keys())[:20]:
        if(len(key.split('_'))==3):
            geo_feature = key.split('_')[0]
            feature_type = key.split('_')[1]
            buffer_size = key.split('_')[2]
        elif(len(key.split('_'))==4):
            geo_feature = key.split('_')[0]
            feature_type = key.split('_')[1]+'_'+key.split('_')[2]
            buffer_size = key.split('_')[3]
        else:
            print("This isn't good")
            exit()
        importance_csv_collector.append([geo_feature,feature_type,buffer_size,result_importance[key]])

    importance_df = pd.DataFrame(importance_csv_collector, columns = ['Geo Feature', 'Feature Type', 'Buffer Size','Importance \(%\)'])

    importance_df.to_csv('feature_importance.csv')

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
    print(args)
    main()
