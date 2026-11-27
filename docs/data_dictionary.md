# Data Dictionary

Cleaned tables in `data/clean`.

## appointments_cleaned.csv (36,000 rows)

| Column | Type | Description | Example |
|---|---|---|---|
| appointment_id | Text | Unique ID of the appointment | APT000126 |
| patient_id | Text | Patient who booked the appointment (FK to patients) | RBP011885 |
| provider_id | Text | Provider who sees the patient (FK to providers) | RBPV0067 |
| facility_id | Text | Facility where the visit is (FK to facilities) | SP03 |
| appointment_weekday | Integer | Day of the week (1 = Monday, 7 = Sunday) | 1 |
| appointment_hour | Integer | Hour of the appointment (24h) | 8 |
| lead_days | Integer | Days between booking and the appointment | 22 |
| visit_type | Text | Type of visit (Acute, Follow-up, Urgent Care, ...) | Behavioral Health |
| specialty_group | Text | Medical specialty of the visit | Behavioral health |
| payer_id | Text | Insurance payer for the visit (FK to payers) | PAY06 |
| reminder_channel | Text | How the reminder was sent (Phone, SMS, Portal, Multi) | Phone |
| reminder_sent_flag | Integer | 1 = reminder sent, 0 = not sent | 1 |
| reminder_days_before | Float | Days before the appointment the reminder was sent | 2.0 |
| same_day_flag | Integer | 1 = booked on the same day as the visit | 0 |
| telehealth_flag | Integer | 1 = telehealth visit, 0 = in-person | 0 |
| distance_to_clinic_miles | Float | Distance from patient to the clinic in miles | 25.2 |
| transportation_barrier_flag | Integer | 1 = patient has a transportation barrier | 0 |
| interpreter_needed_flag | Integer | 1 = patient needs an interpreter | 0 |
| weather_severity_group | Text | Weather on the appointment day (Normal, Rain, Snow, Severe weather) | Normal |
| zip_area_id | Text | Geographic area of the patient | ZA029 |
| patient_age | Integer | Patient age at the appointment | 57 |
| sdoh_risk_score | Float | Social determinants of health risk score (higher = more risk) | 76.6 |
| portal_active_flag | Integer | 1 = patient has an active portal account | 1 |
| deprivation_quintile | Integer | Area deprivation level (1 = least deprived, 5 = most deprived) | 4 |
| prior_completed_visits_12m | Integer | Completed visits in the last 12 months | 0 |
| prior_no_show_count_12m | Integer | Missed visits in the last 12 months | 0 |
| prior_cancel_count_12m | Integer | Cancelled visits in the last 12 months | 0 |
| no_show_flag | Integer | Target: 1 = no-show, 0 = not a no-show | 0 |
| wait_to_room_minutes | Float | Minutes from check-in to exam room (-1 = patient was not seen) | 22.0 |
| cancel_flag | Integer | 1 = appointment was cancelled or rescheduled | 0 |
| appointment_month | Integer | Month of the appointment (1-12) | 1 |
| appointment_day | Integer | Day of the month (1-31) | 1 |

## calendar_cleaned.csv (731 rows)

| Column | Type | Description | Example |
|---|---|---|---|
| year | Integer | Calendar year | 2024 |
| quarter | Integer | Quarter of the year (1-4) | 1 |
| month_num | Integer | Month number (1-12) | 1 |
| weekday_num | Integer | Day of the week (1 = Monday, 7 = Sunday) | 1 |
| weekend_flag | Integer | 1 = weekend | 0 |
| holiday_flag | Integer | 1 = official holiday | 1 |
| flu_season_flag | Integer | 1 = date is in flu season | 1 |

## facilities_cleaned.csv (18 rows)

| Column | Type | Description | Example |
|---|---|---|---|
| facility_id | Text | Unique ID of the facility | HOSP01 |
| facility_name | Text | Facility name | Riverbend Medical Center |
| facility_type | Text | Type of facility (Hospital, ED, Urgent care, clinic, ...) | Hospital |
| zip_area_id | Text | Geographic area of the facility | ZA010 |
| urban_rural_group | Text | Urban core, Suburban, Small town or Rural | Urban core |
| teaching_site_flag | Integer | 1 = teaching site | 1 |
| service_line_focus | Text | Main service of the facility | Acute care hospital |

## patients_cleaned.csv (11,930 rows)

| Column | Type | Description | Example |
|---|---|---|---|
| patient_id | Text | Unique ID of the patient | RBP000001 |
| sex_at_birth | Text | Sex at birth ("Not recorded" filled with the mode) | Female |
| race_ethnicity_group | Text | Race / ethnicity group | Black |
| preferred_language | Text | Language the patient prefers | Spanish |
| interpreter_needed_flag | Integer | 1 = needs an interpreter | 1 |
| zip_area_id | Text | Geographic area where the patient lives | ZA003 |
| payer_primary_id | Text | Primary insurance payer (FK to payers) | PAY04 |
| pcp_provider_id | Text | Primary care provider (FK to providers) | RBPV0019 |
| chronic_condition_count | Integer | Number of chronic conditions | 2 |
| sdoh_risk_score | Float | Social determinants of health risk score (higher = more risk) | 45.2 |

## payers_cleaned.csv (8 rows)

| Column | Type | Description | Example |
|---|---|---|---|
| payer_id | Text | Unique ID of the payer | PAY01 |
| payer_group | Text | Insurance category (Commercial, Medicare, Medicaid, ...) | Commercial |

## providers_cleaned.csv (128 rows)

| Column | Type | Description | Example |
|---|---|---|---|
| provider_id | Text | Unique ID of the provider | RBPV0006 |
| provider_type | Text | Professional type (MD, DO, NP, PA, RN, ...) | RN |
| specialty_group | Text | Medical specialty | Primary care |
| years_in_practice | Integer | Years the provider has practiced | 2 |
| fte_status | Text | Full-time, Part-time or Per diem | Part-time |
| panel_size | Float | Number of patients assigned to the provider | 793.0 |
| language_1 | Text | Main language the provider speaks | English |
| provider_gender | Text | Provider gender | Woman |
| provider_age_band | Text | Provider age group | 45-54 |
