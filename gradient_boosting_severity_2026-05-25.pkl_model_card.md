# Model Card for gradient_boosting_severity_2026-05-25.pkl

This model is a gradient boosting classifier designed to predict road traffic collision severity in Great Britain using STATS19 data. It is part of the UK Collision Severity Prediction project, which focuses on modelling injury outcomes (Fatal, Serious, Slight) from structured collision records published by the UK Department for Transport.

The model was trained using a gradient boosting ensemble method due to its strong performance on tabular, mixed-type datasets and its ability to capture non-linear interactions between road, environmental, and vehicle-related factors. The training pipeline includes preprocessing steps such as categorical encoding, missing value handling, and feature alignment across STATS19’s collision, vehicle, and casualty tables.

This model is documented in accordance with the FAIR4ML metadata specification (T3.3), ensuring transparency of training configuration, feature engineering, and evaluation methodology. It is also packaged within a RO-Crate (T3.1), which provides machine-readable provenance, dataset lineage, and reproducibility metadata for the full machine learning workflow.





#  Table of Contents

- [Model Card for gradient_boosting_severity_2026-05-25.pkl](#model-card-for--model_id-)
- [Table of Contents](#table-of-contents)
- [Model Details](#model-details)
  - [Model Description](#model-description)
- [Uses](#uses)
  - [Direct Use](#direct-use)
  - [Out-of-Scope Use](#out-of-scope-use)
- [Limitations](#Limitations)
- [Training Details](#training-details)
  - [Training Data](#training-data)
- [Evaluation](#evaluation)
- [Ethical Considrations](#ethical-considerations)
# Model Details

## Model Description

This model is a gradient boosting classifier designed to predict road traffic collision severity in Great Britain using STATS19 data. It is part of the UK Collision Severity Prediction project, which focuses on modelling injury outcomes (Fatal, Serious, Slight) from structured collision records published by the UK Department for Transport.

The model was trained using a gradient boosting ensemble method due to its strong performance on tabular, mixed-type datasets and its ability to capture non-linear interactions between road, environmental, and vehicle-related factors. The training pipeline includes preprocessing steps such as categorical encoding, missing value handling, and feature alignment across STATS19’s collision, vehicle, and casualty tables.

This model is documented in accordance with the FAIR4ML metadata specification (T3.3), ensuring transparency of training configuration, feature engineering, and evaluation methodology. It is also packaged within a RO-Crate (T3.1), which provides machine-readable provenance, dataset lineage, and reproducibility metadata for the full machine learning workflow.


- **Language(s) (NLP):** en
- **License:** mit



# Uses

This model is intended for research, transport analytics, and policy-support applications involving historical road collision data. It is suitable for exploring patterns in collision severity and supporting data-driven road safety analysis in the UK context.

The model can be used to estimate severity risk distributions for collisions under similar conditions to the STATS19 dataset. It is intended to assist analysts in identifying contributing factors such as road type, lighting conditions, weather, and vehicle involvement.

The model should be used as a decision-support tool rather than a standalone decision-making system. Outputs are probabilistic and should be interpreted in aggregate rather than as deterministic predictions for individual incidents.


## Direct Use


This model is directly usable for offline inference on structured collision datasets that match the STATS19 schema used during training. It can be loaded from the serialized .pkl file and applied to preprocessed feature vectors to generate severity predictions without additional fine-tuning. Direct use assumes that input data follows the same feature engineering pipeline and encoding scheme defined in the original training workflow.

The model is appropriate for batch prediction tasks, such as retrospective analysis of collision datasets or integration into research dashboards. It is not designed for raw, unprocessed inputs and requires consistent preprocessing to ensure valid outputs. Any deviation in feature format or distribution may degrade performance and should be carefully validated before deployment.

Direct use is intended for research, evaluation, and decision-support contexts where predictions are interpreted probabilistically. Users should not interpret outputs as deterministic or causal statements about individual collision events.


## Out-of-Scope Use


This model is not suitable for real-time safety-critical systems such as autonomous driving, emergency dispatch automation, or active traffic control systems. It has not been validated for operational deployment where incorrect predictions could lead to immediate safety consequences.

The model should not be used for legal liability determination, insurance adjudication, or enforcement decisions. It does not encode causal relationships and should not be interpreted as providing explanations of fault or responsibility.

It is also out of scope to apply this model directly to datasets outside Great Britain or to non-STATS19 schemas without retraining or domain adaptation. Differences in reporting standards and road environments may significantly degrade performance.


# Training Details

## Training Data


This model was trained from processed data sourced from the United Kingdom Government. The processed data culled some data and stratified in a more digestable manner.

DOI: https://doi.org/10.70124/s4hn9-sqv24
 
# Evaluation

## 1. Per-Class Performance (Gradient Boosting)
| Class   | Precision | Recall | F1-Score |
| ------- | --------- | ------ | -------- |
| Fatal   | 0.08      | 0.25   | 0.12     |
| Serious | 0.36      | 0.24   | 0.29     |
| Slight  | 0.78      | 0.83   | 0.81     |

## 2. Model Comparison (Validation Set)
| Model             | Macro F1 | Accuracy |
| ----------------- | -------- | -------- |
| Decision Tree     | 0.37     | 0.58     |
| Random Forest     | 0.38     | 0.65     |
| Gradient Boosting | 0.40     | 0.67     |

# Limitations
The model is limited by the inherent constraints of STATS19 data, which only includes police-reported injury collisions. This introduces reporting bias and excludes non-reported incidents, which may affect generalisation.

Additionally, the model assumes that historical relationships between features and severity remain stable over time. Changes in infrastructure, driving behaviour, or reporting practices may reduce predictive reliability.

# Ethical Considerations
This model operates on sensitive real-world accident data and therefore requires careful ethical handling. Although STATS19 data is anonymised, there remains a risk of indirect bias when combining geographic or socio-demographic features.

The model may reflect or amplify existing biases in reporting practices or road infrastructure inequalities. For example, certain regions or road types may be over- or under-represented in the dataset.

Outputs should not be used to justify discriminatory policy decisions or punitive enforcement targeting specific locations or populations. The model is intended to support safety improvements and research, not enforcement or surveillance.


<details>
<summary> Click to expand </summary>

from transformers import ${model.config?.adapter_transformers?.model_class}

model = ${model.config?.adapter_transformers?.model_class}.from_pretrained(&#34;${model.config?.adapter_transformers?.{model.id}}&#34;)
model.load_adapter(&#34;gradient_boosting_severity_2026-05-25.pkl&#34;, source=&#34;hf&#34;)

</details>
