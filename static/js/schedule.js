document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'ja',
        customButtons: {
            addButton: {
                text: '追加',
                click: function() {
                    showModal();
                }
            }
        },
        headerToolbar: {
            left: 'prev,next today addButton',
            center: 'title',
            right: 'timeGridDay,timeGridWeek,dayGridMonth'
        },
        events: function(fetchInfo, successCallback, failureCallback) {
            fetch('/api/schedules/')
                .then(response => response.json())
                .then(data => {
                    successCallback(data);
                })
                .catch(error => {
                    console.error('Error fetching events:', error);
                    failureCallback(error);
                });
        },
        dateClick: function(info) {
            showModal(info.dateStr);
        },
        eventClick: function(info) {
            editModal(info.event);
        }
    });
    calendar.render();

    function showModal(date) {
        document.getElementById('title').value = '';
        document.getElementById('start').value = date;
        document.getElementById('end').value = date;
        document.getElementById('location').value = '';
        document.getElementById('description').value = '';
        document.getElementById('color').value = 'blue';

        var eventModal = new bootstrap.Modal(document.getElementById('eventModal'), {
            keyboard: false
        });
        eventModal.show();
    }

    function editModal(event) {
        selectedEventId = event.id;
        document.getElementById('title').value = event.title || '';
        document.getElementById('start').value = event.start ? event.start.toISOString().slice(0, 16) : '';
        document.getElementById('end').value = event.end ? event.end.toISOString().slice(0, 16) : '';
        document.getElementById('location').value = event.extendedProps.location || '';
        document.getElementById('description').value = event.extendedProps.description || '';
        document.getElementById('color').value = event.backgroundColor || 'blue';

        var eventModal = new bootstrap.Modal(document.getElementById('eventModal'));
        eventModal.show();
    }

    window.saveEvent = function() {
        var form = document.getElementById('eventForm');
        var formData = new FormData(form);

        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/schedule/create/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            calendar.refetchEvents();
            var eventModal = bootstrap.Modal.getInstance(document.getElementById('eventModal'));
            eventModal.hide();
        })
        .catch(error => console.error("Error saving event to server:", error));
    };

    window.deleteEvent = function(eventId) {
        console.log(`Attempting to delete event with id: ${eventId}`);  // デバッグ用の出力
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/api/delete_schedule/${eventId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('イベントが削除されました');
                location.reload(); // ページをリロードして更新
            } else {
                alert('イベントの削除に失敗しました');
            }
        })
        .catch(error => console.error("Error:", error));
    };
});