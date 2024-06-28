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
                    console.log(data);
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
        document.getElementById('start').value = date ? date + 'T00:00' : '';
        document.getElementById('end').value = date ? date + 'T23:59' : '';
        document.getElementById('location').value = '';
        document.getElementById('description').value = '';
        document.getElementById('color').value = 'blue';
        document.getElementById('event-id').value = '';
        document.getElementById('delete-button').style.display = 'none'; // 非表示にする

        var eventModal = new bootstrap.Modal(document.getElementById('eventModal'), {
            keyboard: false
        });
        eventModal.show();
    }

    function editModal(event) {
        document.getElementById('event-id').value = event.id;
        document.getElementById('title').value = event.title || '';
        document.getElementById('start').value = event.start ? event.start.toISOString().slice(0, 16) : '';
        document.getElementById('end').value = event.end ? event.end.toISOString().slice(0, 16) : '';
        document.getElementById('location').value = event.extendedProps.location || '';
        document.getElementById('description').value = event.extendedProps.description || '';
        document.getElementById('color').value = event.backgroundColor || 'blue';
        document.getElementById('delete-button').style.display = 'inline'; // 表示にする

        var eventModal = new bootstrap.Modal(document.getElementById('eventModal'));
        eventModal.show();
    }

    window.saveEvent = function(eventId=null) {
        var form = document.getElementById('eventForm');
        var formData = new FormData(form);
        var eventId = document.getElementById('event-id').value;
        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(eventId ? `/api/update_schedule/${eventId}/` : '/api/create_schedule/', {
            method: eventId ? 'PUT' : 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(Object.fromEntries(formData))
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                calendar.refetchEvents();
                var eventModal = bootstrap.Modal.getInstance(document.getElementById('eventModal'));
                eventModal.hide();
            } else {
                alert('スケジュールの保存に失敗しました');
            }
        })
        .catch(error => console.error("Error saving event to server:", error));
    };

    window.deleteEvent = function() {
        var eventId = document.getElementById('event-id').value;
        console.log(`Attempting to delete event with id: ${eventId}`);
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
                location.reload();
            } else {
                alert('イベントの削除に失敗しました');
            }
        })
        .catch(error => console.error("Error:", error));
    };
});