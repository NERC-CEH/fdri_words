# Framework for Environmental Time Series Prediction Tools

---

## Variables for Prediction

**Goal:** Define a set of variables representing different environmental domains with varying predictability and sensor characteristics.

### Proposed variables

| Variable       | Expected Predictability | Challenges                                    | Aids                                          |
|----------------|-------------------------|-----------------------------------------------|-----------------------------------------------|
| Temperature    | High                    |                                                            | Diurnal and seasonal cycles, low spacial variabilty, dense networks |
| River Flow     | Medium to High          | River bed changes, rating changes, out of bank behaviour   | Influenced by upstream river flow and precip events. Seasonal cycles |
| Soil Moisture  | Medium                  | Point sensors sensitive to air pockets flooding with water | Influenced by precipitation and evapotranspiration  |
| Wind Speed     | Low to Medium           | Highly variable, gusty behavior                            | Lower spacial variablilty at larger resolutions     |
| Wind direction | Low to Medium           | Highly variable, gusty behavior                            |                                                     |
| Precipitation  | Low                     | False rain. Blockages. Predicting Y/N to precip occuring. Predicting accurate quantities. Difficulty changes with resolution. Low spacial variability | Dense networks, radar |

**General sensor considerations:**
- Sensor drift
- Calibration errors
- Behaviour outside operating conditions (i.e min/max temp)

---

## Framework for Evaluating Prediction Methods

**Goal:** Establish criteria and evaluation process for methods ranging from simple one-to-one relationships to complex AI/ML models.

### Define Evaluation Objectives

#### 1. Method skill
- **Accuracy:** Closeness of predictions to observed values.
- **Robustness:** Performance across different sites or conditions. And/or dealing with missing or erroneous input data.
- **Completeness:** Any limitations to how much data the method can predict.

| Metric                        | Description                                              | Notes                               |
|-------------------------------|----------------------------------------------------------|-------------------------------------|
| RMSE (Root Mean Square Error) | Measures average magnitude of prediction errors          | Sensitive to large errors           |
| MAE (Mean Absolute Error)     | Average absolute difference between predicted and actual | Less sensitive to outliers          |
| Skill scores                  | Performance relative to baseline methods                 | e.g., persistence or climatology    |
| Coverage                      | Percentage of data it is able to predict                 |                                     |


#### 2. Resources
- **Computational:** Computer power and computation time requires
- **Expertise:** Knowledge required to train / implement / run method.
- **Cost:** License / subscription costs. Staff costs.

| Metric                        | Description                                  | Notes                               |
|-------------------------------|----------------------------------------------|-------------------------------------|
| Computational metrics | Runtime, memory usage                        | Reflects efficiency and scalability |
| Expertise             | Specalist required? Training required?       | Can be Y/N for each                 |
| Software costs        | One-off / ongoing costs                      |                                     |
| Personnel costs       | Staff hours for implementation and operation | Hours or £s?                        |


#### 3. Practicalities
- **Ease of use:** How easy to implement, run and update.
- **Transparency:** Explainability of method results (provenance).
- **Interpretability:** How easily the results can be interpreted.
- **Update effects:** How updates to the method, or input, effect provenance.
- **Scalability:** Ability to handle large datasets or multiple variables.

Metrics for these are more qualitative. Perhaps could be summerised with bad, okay or good.



### Proposed method types

| Method Type           | Examples                      | Strengths                            | Limitations                        |
|-----------------------|-------------------------------|--------------------------------------|------------------------------------|
| **Regression**        | Relationships to near-by data | Lightweight, interpretable           | May miss complex patterns          |
| **Interpolation**     |                               | Lightweight, interpretable           | Bad for data with high variability |
| **Physical Models**   | Hydrological models           | Based on domain knowledge            | Require detailed inputs, complex   |
| **Machine Learning**  | Random Forest, SVM            | Capture nonlinearities, flexible     | Require tuning, less interpretable |
| **Deep Learning / AI**| LSTM, Transformer, CNN        | Handle complex temporal dependencies | Data-hungry, computationally heavy |
| **Hybrid Approaches** | Combination of above          | Balance domain knowledge and data-driven insights | Complex to implement  |

There are a number of timeseries prediction AI tools out there that should be investigated. A good resource for finding these:
https://huggingface.co/models?pipeline_tag=time-series-forecasting&sort=trending

Good starting point--this paper and references therein:
- Schmidt, J.Q., Kerkez, B., 2023. Machine Learning-Assisted, Process-Based Quality Control for Detecting Compromised Environmental Sensors. Environ. Sci. Technol. 57, 18058–18066. https://doi.org/10.1021/acs.est.3c00360


---