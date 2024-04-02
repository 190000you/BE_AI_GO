from Preprocessing import df_filter, categorical_features_names
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor, Pool

train_data, test_data = train_test_split(df_filter, test_size=0.2, random_state=42)

train_pool = Pool(train_data.drop(['DGSTFN'], axis=1),
                  label=train_data['DGSTFN'],
                  cat_features=categorical_features_names)

test_pool = Pool(test_data.drop(['DGSTFN'], axis=1),
                 label=test_data['DGSTFN'],
                 cat_features=categorical_features_names)

model = CatBoostRegressor(
    loss_function='RMSE',
    eval_metric='MAE', #min absolute error
    task_type='CPU',
    depth=6, #높아질수록 정확도가 높아지지만 속도가 느려진다
    learning_rate=0.01,
    n_estimators=2000)

model.fit(
    train_pool,
    eval_set=test_pool,
    verbose=500,
    plot=True)

model_path = "catboost_model.dump"
model.save_model(model_path)