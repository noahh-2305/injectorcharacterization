import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy as sci
import numpy as np

data = pd.read_excel("D:\\Programming\\InjectorTesting\\Results.xlsx")

reduced_data = data[["Duty Cycle", "RPM Equivalent", "mg per Injection"]]

x=reduced_data["Duty Cycle"].values
y=reduced_data["RPM Equivalent"].values
z=reduced_data["mg per Injection"].values

interpolator_1 = sci.interpolate.LinearNDInterpolator((x,y),z)
interpolator_2 = sci.interpolate.NearestNDInterpolator(list(zip(x,y)),z)

print(interpolator_1(0.85,2000))

def interpolator(x,y):
    if type(x) is not np.ndarray and type(y) is not np.ndarray:
        temp = interpolator_1(x,y)
        return temp if not pd.isnull(temp) else interpolator_2(x,y)
    else:
        temp1 = interpolator_1(x,y)
        temp2 = interpolator_2(x,y)
        df_1 = pd.DataFrame(temp1)
        df_2 = pd.DataFrame(temp2)
        df = df_1.fillna(value=df_2)
        return df.values

fig = px.scatter_3d(data, x="Duty Cycle", y="RPM Equivalent", z="mg per Injection",
    labels = {
        "Duty Cycle": "Duty Cycle",
        "RPM Equivalent": "RPM",
        "mg per Injection": "Injection Mass (mg)"
        })

fig.update_layout(
    title=dict(text="Denso 297500-1060 Raw Mass Profile")
)

x_interp = np.linspace(0,1,11)
y_interp = np.linspace(2000,14000,13)

z_points = np.meshgrid(x_interp,y_interp)

print(interpolator(0.85,2000))

z_interp = interpolator(z_points[0],z_points[1])

fig2 = go.Figure(
    data = go.Surface(
        x=x_interp,
        y=y_interp,
        z=z_interp
    )
)

fig2.update_layout(
    title=dict(text="Denso 297500-1060 Interpolated Mass Profile")
)

fig2.update_scenes(xaxis_title_text="Duty Cycle",  
                  yaxis_title_text="RPM",  
                  zaxis_title_text="Injection Mass (mg)")

fig.show()
fig2.show()