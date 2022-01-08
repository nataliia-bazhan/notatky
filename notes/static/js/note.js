'use strict';
document.addEventListener('DOMContentLoaded', () => {
  const stickyArea = document.querySelector(
    '#stickies-container'
  );

  const createStickyButton = document.querySelector(
    '#createsticky'
  );

  const deleteSticky = e => {
    if (confirm("Are you sure you want to delete this note?")){
    const sticker = e.target.parentNode;
    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
            type: 'POST',
            url: "/delete_note/",
            headers: {
                   'X-CSRFToken': csrftoken
            },
            data: {
                'id': sticker.id,
            },
            success: function (response) {
                //alert(response['message'])
            },
            error: function (response) {
                //alert(response["responseJSON"]["error"]);
            }
        });
    sticker.remove();
    };
  };

  const saveSticky = e => {
    const sticker = e.target.parentNode;
    const title = document.getElementById(`title_${sticker.id}`).value;
    const content = document.getElementById(`content_${sticker.id}`).value;
    const left = sticker.style.left;
    const top = sticker.style.right;
    //const footer = document.getElementById(`footer_${sticker.id}`);

    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
            type: 'POST',
            url: "/update_note/",
            headers: {
                   'X-CSRFToken': csrftoken
            },
            data: {
                'id': sticker.id,
                'title': title,
                'content': content,
                'left': left,
                'top': sticker.style.top,

            },
            success: function (response) {
                if (!response['saved']) {
                    $(`#save_alert_${sticker.id}`).css('color', 'red');
                    $(`#save_alert_${sticker.id}`).text('note wasn\'t changed!');
                    $(`#save_alert_${sticker.id}`).fadeIn('fast');
                    window.setTimeout(function(){
                                     $(`#save_alert_${sticker.id}`).fadeOut('fast');}, 3000);
                } else {
                    $(`#save_alert_${sticker.id}`).css('color', 'green');
                    $(`#save_alert_${sticker.id}`).text('note successfully changed!');
                    $(`#save_alert_${sticker.id}`).fadeIn('fast');
                    $(`#footer_${sticker.id}`).fadeOut('fast');
                    //alert($(`#footer_${sticker.id} span`).innerHTML)
                    window.setTimeout(function(){
                                     $(`#save_alert_${sticker.id}`).fadeOut('fast');}, 3000);
                }
            },
            error: function (response) {
                alert(response["error"]);
            }
        });
  };

  let isDragging = false;
  let dragTarget;

  let lastOffsetX = 0;
  let lastOffsetY = 0;

  function drag(e) {
    if (!isDragging) return;
    dragTarget.style.left = e.clientX - lastOffsetX + 'px';
    dragTarget.style.top = e.clientY - lastOffsetY + 'px';
  }

  function createSticky() {
    const newSticky = document.createElement('div');
    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    const response = $.parseJSON($.ajax({
                                      url: "/create_note/",
                                      headers: {
                                                 'X-CSRFToken': csrftoken
                                               },
                                      type: 'POST',
                                      dataType: "json",
                                      async: false
                                      }).responseText);
    newSticky.setAttribute("id", response.id);
    const html = '<div id=' + `save_alert_${response.id}` + ' class="save_alert">note wasn\'t changed</div>' +
                 '<h3><input type="text" name="stickytitle" id=' + `title_${response.id}` + '></h3>\n' +
                 '<p><textarea name="stickytext" id=' + `content_${response.id}` + ' cols="24" rows="10"></textarea></p>\n' +
                 '<span class="deletesticky">&times;</span>\n' +
                 '<span class="savesticky">&#10003;</span>';
    newSticky.classList.add('drag', 'sticky');
    newSticky.innerHTML = html;
    stickyArea.append(newSticky);
    positionSticky(newSticky);
    applyDeleteListener();
    applySaveListener();
  }

  function positionSticky(sticky) {
    sticky.style.left =
      window.innerWidth / 2 -
      sticky.clientWidth / 2 +
      (-100 + Math.round(Math.random() * 50)) +
      'px';
    sticky.style.top =
      window.innerHeight / 2 -
      sticky.clientHeight / 2 +
      (-100 + Math.round(Math.random() * 50)) +
      'px';
  }

  function applyDeleteListener() {
    let deleteStickyButtons = document.querySelectorAll(
      '.deletesticky'
    );
    deleteStickyButtons.forEach(dsb => {
      dsb.removeEventListener('click', deleteSticky, false);
      dsb.addEventListener('click', deleteSticky);
    });
  }

  function applySaveListener() {
    let saveStickyButtons = document.querySelectorAll(
      '.savesticky'
    );
    saveStickyButtons.forEach(dsb => {
      dsb.removeEventListener('click', saveSticky, false);
      dsb.addEventListener('click', saveSticky);
    });
  }

  window.addEventListener('mousedown', e => {
    if (!e.target.classList.contains('drag')) {
      return;
    }
    dragTarget = e.target;
    dragTarget.parentNode.append(dragTarget);
    lastOffsetX = e.offsetX;
    lastOffsetY = e.offsetY;
    // console.log(lastOffsetX, lastOffsetY);
    isDragging = true;
  });

  window.addEventListener('mousemove', drag);
  window.addEventListener('mouseup', () => (isDragging = false));

  createStickyButton.addEventListener('click', createSticky);
  applyDeleteListener();
  applySaveListener();
});