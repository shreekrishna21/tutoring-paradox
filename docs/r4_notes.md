# Tutoring project notes

A school district offered free tutoring to improve pass rates, but the tutored students ended up failing more often than other students. 
Administrators are ready to cut the program's funding,
 so our job is to find out what's driving the failures so they can make an informed/educated decision. 

How the program works: 
 * Tutoring is free and voluntary. 
 * Teachers and counselors refer students they're concerned about, 
and parents and students can also ask for a place. 
 * Each referred student gets a fixed weekly 45-minute session at their
own school, in groups of up to four, until the end of the year.
 * Sessions are after the last bell, and the district runs no late 
buses. 

There is a file "first_look.py" that takes the district's 
separte files, combines them into one table, and prints failure
rates three different ways.
   1) Overall, 2) Within GPA groups, 3) By term 

This is the result from that data. 

## 1) Overall
Share of grades that were failures in math, English and science.

```text
              mean    size
referred
False     0.096073  315249
True      0.239101   44751
```

Referred: 23.9%. Not referred: 9.6%.



## 2) Within GPA groups

`gpa_band` is a feature created from `prior_year_gpa`. It groups students by their prior GPAs from the year before. It acts as a baseline for students at the same level who were referred vs not referred

`mean` is the share of grades that were failures
`size` is the number of grade rows 
`referred` shows whether the student was referred in the subject or not
 
We use prior GPA because it comes from 2024-25, before this year's referrals. If referred students were already struggling, comparing everyone at once could mix up the effect of tutoring with where students started.

```text
                            mean    size
gpa_band      referred
(-0.001, 1.0] False     0.936869     396
              True      0.863889    1440
(1.0, 2.0]    False     0.512294   22491
              True      0.430404   16524
(2.0, 3.0]    False     0.112355  145548
              True      0.100510   21978
(3.0, 4.0]    False     0.005807  137241
              True      0.005063    3555
NaN           False     0.129949    9573
              True      0.093301    1254
```

The referred failure rate is lower in every GPA group, including the blank GPA group.




## 3) By term

```text
referral_term
1    10750
2     2788
3     1379

term                  1         2         3
referral_term
1              0.237674  0.237488  0.196837
2              0.342181  0.258967  0.190459
3              0.347353  0.369108  0.203771

Not referred, by term
1    0.094934
2    0.104698
3    0.088587
```

Students referred in terms 2 and 3 failed far more often than 
non-referred students before referral. Their failure rates were
lower by term 3.

## 4) Attendance 
Cleaning the session log: 
 * Removed extra space from subject labels: pairs went from 25,883 to 14,917.
 * Removed 2,480 exact copies: rows went from 415,850 to 413,370.
 * 42 rows have odd `minutes` values (8 Present with 0, plus 450, 455 and 4500). Rates use `attendance`, not `minutes`.

 ### How attendance was calculated 
 Script: `attendance.py`. Data: `tutoring_sessions.csv.gz` and `students.csv`

### Attendance results

`attendance_rate` is sessions attended divided by sessions schedules, for each student in each subject. The mean is the average of those rates across student-subject pairs

 attendance_rate = sessions attended / sessions scheduled 

| Group | Mean attendance | Pairs |
|---|---|---|
| All referred pairs | 56.8% | 14,917 |
| Bus riders | 53.4% | 9,105 |
| Non-riders | 62.1% | 5,812 |

Referred students attended a little over half of their scheduled sessions on average, and bus riders attended less often than non-riders. This doesn't prove that buses cause lower attendance.


### Failure rate by attendance

| Sessions attended | Term 3 failure rate | Pairs |
|---|---|---|
| 0-25% | 35.3% | 1,874 |
| 25-50% | 27.2% | 4,085 |
| 50-75% | 14.4% | 5,002 |
| 75-100% | 11.0% | 3,956 |

Higher attendance went with lower failure. This is a pattern, not proof that attending causes lower failure. Attendance happens after referral, and prior GPA is not accounted for here.

## Features

| Feature | How it's made | Why | Known when |
|---|---|---|---|
| `failed` (target) | F in term 1, below 60 in terms 2 and 3 | Input 4 defines a failing grade; this is what we're trying to explain | End of each term |
| `referred` (treatment) | Student has a referral in that subject | Input 1: this is how students enter the program | At referral |
| `gpa_band` | `prior_year_gpa` grouped as 0-1, 1-2, 2-3, 3-4, or blank | Input 5: compares students who started at similar levels | Before the school year |
| `referral_term` | `referral_date` matched to the term dates | Separates grades from before and after referral | At referral |
| `attendance_rate` | Sessions attended / sessions scheduled, per student and subject | Inputs 2 and 3: referred doesn't mean attended | After referral |
| `bus_rider` | From `students.csv` | Input 6: no late buses may limit attendance | Student record |

## Limits
* These results don't prove tutoring works.
* The referral term's grade can mix before and after referral.
* Term 1 referrals have no earlier term in this data.
* Sections 1-3 count referrals, not sessions attended.
* The data doesn't record why students were referred.
* Students who left the district during the year are not in the export.

## AI use
Used Claude to help write the analysis scripts and interpret the output.

