function delete_notification(id) {
  document.getElementById(id).remove();
  emtpy_check();
}

function emtpy_check() {
  if (
    document.querySelector(".notification-wrapper ul").innerHTML.trim() != ""
  ) {
    let element = document.getElementById("notification_icon");
    element.classList.add("active");
    document.getElementById("notification_button").style.cursor = "pointer";
  } else {
    let ul = document.getElementById("notification_list");
    ul.remove();
    let element = document.getElementById("notification_icon");
    element.classList.remove("active");
    document.getElementById("notification_button").disabled = true;
    document.getElementById("notification_button").style.cursor = "default";
  }
}

emtpy_check();
if (document.querySelector(".notification-wrapper ul")) {
  if (
    document.querySelector(".notification-wrapper ul").innerHTML.trim() != ""
  ) {
    let element = document.getElementById("notification_list");
    let layer = document.querySelector(".layer");
    element.classList.add("active");
    layer.classList.add("active");
  }
}
