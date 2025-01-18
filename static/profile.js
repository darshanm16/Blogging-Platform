function deleteblog(id) {
  var con = document.getElementById("confirm");
  con.style.visibility = "visible";
  document.getElementById("cancel").onclick = function () {
    con.style.visibility = "hidden";
  };

  document.getElementById("yes").onclick = function () {
    con.style.visibility = "hidden";
    fetch("/profile/modify-blog/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: id }),
    })
      .then((response) => {
        if (response.ok) {
          location.reload();
        } else {
          alert("Failed to delete the blog.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while deleting the blog.");
      });
  };
}

function editblog(id) {
  var blogid = "blog" + id;
  var blog = document.getElementsByClassName(blogid);
  for (var i = 0; i < blog.length; i++) {
    if (blog[i].style.display == "") {
      blog[i].style.display = "none";
    } else {
      blog[i].style.display = "";
    }
  }
}

function updateblog(id) {
  var title = document.getElementById("title" + id).value.trim();
  var content = document.getElementById("content" + id).value.trim();

  if (!title || !content) {
    alert("Title or content element not found.");
    return;
  }

  fetch("/profile/modify-blog/", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: id, title: title, content: content }),
  })
    .then((response) => {
      if (response.ok) {
        location.reload();
      } else {
        return response.json().then((data) => {
          alert(data.message || "Failed to edit the blog.");
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while editing the blog.");
    });
}
