import matching_Phase
import functions
import constants
from dbconnection import db
from datetime import datetime

document_no = 0
#strUTT = input("Enter UTT: ")
UTT = 20#int(strUTT)
#riderCheck = input("Enter Total No of Riders To Be Checked: ")
riderCheck_int = 600#int(riderCheck)
trip_ids = []
k=0
debut = 1
fin = 2
for i in range(debut, fin):
    ridersMatchingCount = 0
    ridersMatchedCount = 0
    requiredDriversCount = 0
    totalRidersInPool = 0
    exact_match = 0
    diff_match = 0
    avg_rider_wait_time = 0
    count_of_user = 0
    time_start = datetime.now().strftime(constants.TIME_STRING)
    actual_time_start = datetime.now()

    while ridersMatchingCount < riderCheck_int:
                k=k+1
                print("results",k)
                print(ridersMatchingCount)
                ridersMatching, ridersMatched, requiredDrivers, exact_close_match, different_char_match, tripId, avg_waiting_time, usercount = matching_Phase.mainResults(
                    UTT, riderCheck_int)
                print("Pour les passager traverser :", ridersMatching, "passager accepter :", ridersMatched, "le nombre de driver :", requiredDrivers)
                print("exact close match", exact_close_match, "alternatif match", different_char_match)
                ridersMatchingCount += ridersMatching
                ridersMatchedCount += ridersMatched
                requiredDriversCount += requiredDrivers
                totalRidersInPool += ridersMatched
                avg_rider_wait_time += avg_waiting_time
                count_of_user += usercount
                exact_match += exact_close_match
                diff_match += different_char_match
                trip_ids.append(tripId)
                avg = avg_rider_wait_time/count_of_user
                avg = round(avg, 2)

    time_end = datetime.now().strftime(constants.TIME_STRING)
    actual_time_end = datetime.now()
    diff_secs, diff_mins = functions.time_diff(actual_time_start, actual_time_end)
    average_rider_waiting_time_of_simulation = (avg_rider_wait_time / count_of_user)
    average_rider_waiting_time_of_simulation = round(average_rider_waiting_time_of_simulation, 2)
    matching_rate = totalRidersInPool/riderCheck_int
    document = {
                constants.TOTAL_RIDERS_CHECKED: ridersMatchingCount,
                constants.TOTAL_RIDERS_MATCHED: ridersMatchedCount,
                constants.TOTAL_RIDERS_IN_POOL: totalRidersInPool,
                "exact_match_count": exact_match,
                "diff_match_count": diff_match,
                constants.FOR_RIDER_COUNT: riderCheck_int,
                "matching_rate": matching_rate,
                "average_rider_waiting_time": average_rider_waiting_time_of_simulation,
                constants.TOTAL_DRIVERS: requiredDriversCount,
                constants.UTT: UTT,
                "tripQs": trip_ids,
                constants.TRIP_START_TIME: time_start,
                constants.TRIP_END_TIME: time_end,
                constants.TRIP_DIFF_SECS: diff_secs,
                constants.TRIP_DIFF_MINS: diff_mins
            }
    print(document)

    results_phase1 = db.resultsCollection1
    doc_id = results_phase1.insert_one(document)

