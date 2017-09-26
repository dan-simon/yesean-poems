// [One should assume that the year/month/day stuff is not there, and is replaced
// by a simpler implementation that uses native-to-JS weeks and cycles.]

var two_digits = (x) => x.toString().padStart(2, '0');

var format_time_main = (day_part, lesser_part, cycle_part) => `The day and time are ${day_part}, ${lesser_part} (${cycle_part})`;

// Day 0 is the first day of a zero week.
var get_day_from_start = (time) => gregorian_to_ce_day(...get_ymd(time)) + 1373286;

var get_week_length = (x) => 5 + (x % 14 == 0) + (x % 720 == 0);

var month_lengths_array = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

var range_5040 = Array.apply(null, Array(5040));

var week_lengths_array = range_5040.map((_, i) => get_week_length(i));

var days_before_each_week = range_5040.map((_, i) => week_lengths_array.slice(0, i).reduce((a, b) => a + b, 0))

var cycle_length = week_lengths_array.reduce((a, b) => a + b, 0)

var get_ymd = (time) => [time.getYear() + 1900, time.getMonth(), time.getDate()];

var days_in_year = (month, day) => day + month_lengths_array.slice(0, month).reduce((a, b) => a + b, 0);

var gregorian_to_ce_day = (year, month, day, ly = month <= 2 ? year - 1 : year) => year * 365 + days_in_year(month, day) +
    Math.floor(ly / 4) - Math.floor(ly / 100) + Math.floor(ly / 400);

var format_time_day = (day) => get_week_and_day(day);

var format_time_cycle = (day) => `${get_cycle(day)} cycles from the start of the calendar`;

var get_weeks_and_days = (day, weeks_before_day = days_before_each_week.filter((i) => i <= day).length - 1) =>
    [weeks_before_day, day - days_before_each_week[weeks_before_day]]

var get_week_and_day = (day, [weeks, days_in_week] = get_weeks_and_days(day % cycle_length)) =>
    is_weekend(weeks, days_in_week) ? `weekend ${get_weekend(weeks)}` : `week ${weeks}, day ${get_day(days_in_week)}`;

var get_cycle = (day) => Math.floor(day / cycle_length);

var is_weekend = (weeks, days_in_week) => days_in_week === get_week_length(weeks) - 1;

var get_weekend = (weeks) => `${weeks}/${(weeks + 1) % 5040}`;

// So that the first day of a week is day 1.
var get_day = (days_in_week) => days_in_week + 1;

var format_time_lesser = (time) => `${time.getHours()}:${two_digits(time.getMinutes())}:${two_digits(time.getSeconds())}`;

var put_in_time_el = (x) => {document.getElementById('time').innerHTML = x};

var display_time = (time = new Date()) => put_in_time_el(format_time_main(
    format_time_day(get_day_from_start(time)),
    format_time_lesser(time),
    format_time_cycle(get_day_from_start(time))));

window.onload = () => setInterval(display_time, 100);

