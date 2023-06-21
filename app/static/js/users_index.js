
const myModalEl = document.getElementById('deleteModal')
myModalEl.addEventListener('show.bs.modal', event => {
    var event_dataset = event.relatedTarget.dataset;
    var deleteUrl = event_dataset.url;
    document.getElementById('deleteActionId').action = deleteUrl;
    document.getElementById('deleteTargetUser').innerHTML = event_dataset.targetLogin;
});
// Event	Description
// hide.bs.modal	This event is fired immediately when the hide instance method has been called.
// hidden.bs.modal	This event is fired when the modal has finished being hidden from the user(will wait for CSS transitions to complete).
// hidePrevented.bs.modal	This event is fired when the modal is shown, its backdrop is static and a click outside of the modal is performed.The event is also fired when the escape key is pressed and the keyboard option is set to false.
// show.bs.modal	This event fires immediately when the show instance method is called.If caused by a click, the clicked element is available as the relatedTarget property of the event.
// shown.bs.modal	This event is fired when the modal has been made visible to the user(will wait for CSS transitions to complete). If caused by a click, the clicked element is available as the relatedTarget property of the event.