**Problem statement:**

Missed appointments are a constant drain on healthcare providers. Each no-show leaves a clinic slot empty, wastes staff time and reduces how efficiently the service runs. Management has no clear picture of why patients miss their visits, or of which upcoming appointments are most likely to be missed. Without that insight, the organization cannot act early, for example by sending targeted reminders or adjusting its scheduling, to reduce no-shows.

**Project objectives:**

- Analyze healthcare appointment data to identify patterns and trends in patient attendance.
- Identify patient, appointment, and location-related factors associated with no-shows.
- Develop and evaluate machine learning models to predict missed appointments.
- Build an interactive dashboard to visualize attendance metrics and no-show patterns.
- Provide data-driven insights to support better appointment scheduling and resource utilization.

**Business questions:**

- Are appointment reminders more effective for certain patient groups based on age, preferred language, and portal activity?
- How do insurance type, copayment amount, and geographical socioeconomic factors relate to appointment attendance?
- Are patients with a history of missed appointments more likely to miss appointments when they have longer booking lead times?
- Are patients with a history of missed appointments more likely to miss future appointments, especially when booking lead times are longer?
- How do transportation barriers, distance, and geographical deprivation interact to influence appointment attendance?

**Dataset:**

Link:[ https://yar177.github.io/intro-to-HDA-site/data-dictionaries.html#dict-ds1-patient-dim-csv](https://yar177.github.io/intro-to-HDA-site/data-dictionaries.html#dict-ds1-patient-dim-csv)

Number of rows: 36K

Number of columns:

| Table name  | Column name                  | Meaning                                                                                                                                       |
| ----------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Patient     | Patient_id                   | A unique ID assigned to each patient.                                                                                                         |
| Patient     | Sex_at_birth                 | The patient's sex recorded at birth.                                                                                                          |
| Patient     | preferred_language           | The language the patient prefers to communicate in.                                                                                           |
| Patient     | interpreter_needed_flag      | Indicates whether the patient needs an interpreter (1 = Yes, 0 = No).                                                                         |
| Patient     | race_ethnicity_group         | Patient's race and ethnicity group.                                                                                                           |
| Patient     | zip_area_id                  | Identifies the geographical area where the patient lives.                                                                                     |
| Patient     | payer_primary_id             | Identifies the patient's primary insurance provider or payer.                                                                                 |
| Patient     | pcp_provider_id              | Identifies the patient's primary care provider.                                                                                               |
| Patient     | chronic_condition_count      | The number of chronic health conditions the patient has.                                                                                      |
| patient     | sdoh_risk_score              | A score representing the patient's social determinants of health risks. A higher score indicates greater risk.                                |
| Provider    | provider_id                  | A unique ID assigned to each healthcare provider.                                                                                             |
| Provider    | provider_type                | The provider's professional type, such as MD, NP, or PA.                                                                                      |
| Provider    | specialty_group              | The medical specialty or department the provider works in.                                                                                    |
| Provider    | years_in_practice            | The number of years the provider has been practicing.                                                                                         |
| Provider    | fte_status                   | Indicates the provider's working status, such as Full-time, Part-time, or Per diem.                                                           |
| Provider    | panel_size                   | The number of patients assigned to the provider.                                                                                              |
| Provider    | Lang1&lang2                  |                                                                                                                                               |
| Provider    | provider_gender              | The provider's gender.                                                                                                                        |
| Provider    | provider_age_band            | The provider's age category or group.                                                                                                         |
| Facility    | facility_id                  | A unique ID assigned to each healthcare facility.                                                                                             |
| Facility    | facility_name                | The name of the healthcare facility.                                                                                                          |
| Facility    | facility_type                | The type of facility, such as Hospital, Emergency Department, Urgent Care, or Clinic.                                                         |
| Facility    | zip_area_id                  | Identifies the geographical area associated with the facility.                                                                                |
| Facility    | urban_rural_group            | Classifies the facility's location as Urban, Suburban, Small Town, or Rural.                                                                  |
| Facility    | teaching_site_flag           | Indicates whether the facility is a teaching site (1 = Yes, 0 = No).                                                                          |
| Facility    | service_line_focus           | The main medical service or specialty provided by the facility.                                                                               |
| payer       | Payer_id                     | A unique ID assigned to each insurance payer.                                                                                                 |
| payer       | payer_group                  | The general insurance category, such as Commercial, Medicare, or Medicaid.                                                                    |
| Calendar    | calendar_date                | The actual calendar date.                                                                                                                     |
| Calendar    | Quarter                      | The quarter of the year (1–4).                                                                                                                |
| Calendar    | month_num                    | The name of the month.                                                                                                                        |
| Calendar    | weekday_num                  | The day number of the week (1 = Monday, 7 = Sunday).                                                                                          |
| Calendar    | weekend_flag                 | Indicates whether the date falls on a weekend (1 = Yes, 0 = No).                                                                              |
| Calendar    | holiday_flag                 | Indicates whether the date is an official holiday (1 = Yes, 0 = No).                                                                          |
| Calendar    | flu_season_flag              | Indicates whether the date falls within the flu season (1 = Yes, 0 = No).                                                                     |
| Appointment | appointment_id               | A unique ID assigned to each appointment.                                                                                                     |
| Appointment | patient_id                   | Identifies the patient associated with the appointment.                                                                                       |
| Appointment | provider_id                  | Identifies the healthcare provider responsible for the appointment.                                                                           |
| Appointment | facility_id                  | Identifies the facility where the appointment is scheduled.                                                                                   |
| Appointment | payer_id                     | Identifies the patient's insurance payer for the appointment.                                                                                 |
| Appointment | appointment_created_datetime | The date and time when the appointment was booked.                                                                                            |
| Appointment | appointment_datetime         | The scheduled date and time of the appointment.                                                                                               |
| Appointment | lead_days                    | The number of days between booking the appointment and its scheduled date.                                                                    |
| Appointment | visit_type                   | The type of medical visit, such as Acute, Behavioral Health, or Urgent Care.                                                                  |
| Appointment | specialty_group              | The medical specialty or department related to the appointment.                                                                               |
| Appointment | reminder_channel             | The communication method used to send the appointment reminder, such as Phone or SMS.                                                         |
| Appointment | reminder_sent_flag           | Indicates whether a reminder was sent to the patient (1 = Yes, 0 = No).                                                                       |
| Appointment | reminder_days_before         | The number of days before the appointment when the reminder was sent.                                                                         |
| Appointment | same_day_flag                | Indicates whether the appointment was booked on the same day as the scheduled visit (1 = Yes, 0 = No).                                        |
| Appointment | telehealth_flag              | Indicates whether the appointment is conducted remotely (1 = Yes, 0 = No).                                                                    |
| Appointment | copay_usd                    | The amount the patient is expected to pay for the appointment in US dollars.                                                                  |
| Appointment | distance_to_clinic_miles     | The distance between the patient's location and the healthcare facility in miles.                                                             |
| Appointment | transportation_barrier_flag  | Indicates whether the patient has a recorded transportation barrier (1 = Yes, 0 = No).                                                        |
| Appointment | weather_severity_group       | A category describing the severity of weather conditions on the appointment date.                                                             |
| Appointment | zip_area_id                  |                                                                                                                                               |
| Appointment | patient_age                  | The patient's age at the time of the appointment.                                                                                             |
| Appointment | portal_active_flag           | Indicates whether the patient has an active patient portal account (1 = Yes, 0 = No).                                                         |
| Appointment | prior_completed_visits_12m   | The number of appointments the patient completed during the previous 12 months.                                                               |
| Appointment | prior_no_show_count_12m      | The number of appointments the patient missed during the previous 12 months.                                                                  |
| Appointment | prior_cancel_count_12m       | The number of appointments the patient canceled during the previous 12 months.                                                                |
| Appointment | check_in_datetime            | The date and time when the patient checked in at the facility.                                                                                |
| Appointment | seen_datetime                | The date and time when the patient was seen by the healthcare provider.                                                                       |
| Appointment | cancel_datetime              | The date and time when the appointment was canceled. It is NULL if the appointment was not canceled.                                          |
| Appointment | attendance_outcome           | The final attendance result, such as Completed, No-show, or Canceled.                                                                         |
| Appointment | no_show_flag                 | The target variable indicating whether the patient missed the appointment (1 = No-show, 0 = Not a no-show).                                   |
| Appointment | arrival_late_minutes         | The number of minutes the patient arrived early or late. Negative values indicate early arrival, while positive values indicate late arrival. |
| Appointment | wait_to_room_minutes         | The number of minutes between patient check-in and being moved to the examination room.                                                       |

---

**Dashboard plan:**

- Show vs. no-show pie chart
- No-show categorized by zip area chart
- Show vs. no-show categorized by doctor speciality group
- Show vs. no-show categorized by quarters, weekends, flu_season and holidays.

**Tools:**

- Python
- SQL
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Plotly
- Dash
- Git
