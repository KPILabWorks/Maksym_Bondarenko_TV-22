import numpy as np
import pandas as pd
import bambi as bmb
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Генерація даних для навчання моделей
np.random.seed(322)
X = np.random.uniform(0, 40, 100)  # Температура
Y = 100 - 2 * X + np.random.normal(0, 5, 100)  # Витрати енергії
df = pd.DataFrame({'Temperature': X, 'Energy': Y})
train_df, test_df = train_test_split(df, test_size=0.2)

# Звичайна лінійна регресія
lin_reg = LinearRegression()
lin_reg.fit(train_df[['Temperature']], train_df['Energy'])
Y_pred_lin = lin_reg.predict(test_df[['Temperature']])
mse_lin = mean_squared_error(test_df['Energy'], Y_pred_lin)
print(f'MSE (Classical Regression): {mse_lin:.4f}')

# Баєсівська лінійна регресія
model = bmb.Model("Energy ~ Temperature", data=train_df)
fitted = model.fit()
posterior_samples = fitted.posterior
alpha_post = posterior_samples["Intercept"].mean().item()
beta_post = posterior_samples["Temperature"].mean().item()
Y_pred_bayes = alpha_post + beta_post * test_df["Temperature"]
mse_bayes = mean_squared_error(test_df["Energy"], Y_pred_bayes)
print(f'MSE (Bayesian Regression): {mse_bayes:.4f}')

# Visualization
plt.scatter(test_df["Temperature"], test_df["Energy"], label='Actual Data')
plt.plot(test_df["Temperature"], Y_pred_lin, label='Linear Regression', color='red')
plt.plot(test_df["Temperature"], Y_pred_bayes, label='Bayesian Regression', color='green')
plt.legend()
plt.xlabel('Temperature')
plt.ylabel('Energy Consumption')
plt.title('Comparison of Regression Models')
plt.show()
