document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'ja',
        events: '{% url "core:events" %}',
        dayMaxEvents: true, // イベントが多い日には「もっと見る」を表示
        eventContent: function(arg) {
            if (arg.event.extendedProps.category_color) {
                arg.backgroundColor = arg.event.extendedProps.category_color;
            }
        },
        dayCellContent: function(arg) {
            if (arg.isWeekend) {
                arg.dayNumberText = `<span style="color: ${arg.date.getDay() === 6 ? 'blue' : 'red'}">${arg.dayNumberText}</span>`;
            }
        },
        dateClick: function(info) {
            // 日付をクリックした時の動作（スケジュール追加など）
        },
        eventClick: function(info) {
            window.location.href = info.event.url; // イベントに関連付けられたURLへリダイレクト
        }
    });
    calendar.render();
});