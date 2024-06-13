document.addEventListener("DOMContentLoaded", function() {
    const taskForm = document.getElementById("task-form");
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; // CSRFトークンを取得

    taskForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const formData = new FormData(taskForm);
        formData.append('csrfmiddlewaretoken', csrftoken); // FormDataにCSRFトークンを追加

        fetch("/tasks/add/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrftoken, // リクエストヘッダーにCSRFトークンを含める
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // 成功した場合の処理
        })
        .catch(error => console.error("Error:", error));
    });
});