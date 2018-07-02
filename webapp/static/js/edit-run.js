/*
    Created by Jack Allcock 21/06/2018
    This javascript file handles the edit PV's modal
*/

$(document).ready(function(e){

    // Get the modal so that we can hide/un-hide and attach the ID
    var modal = $(".modal");

    // On the click of the Modal Close button, hide the modal and refresh the page.
    $(".close").click(function(event){
        // Fade out 500ms
        modal.fadeOut(500);
    });

    // When the edit button is clicked, get the ID from the button attribute
    // Show the modal and change the input fields value to the ID
    $(".pv-edit-button").click(function(event){

        // Fade in 500ms
        modal.fadeIn(500);

        variableId = this.id;
        // Create array of all the table rows
        rows = $('.table--row');
        var data = [];

        // For each row, look at each column, get the ID and check the ID to the one user selected
        // Then get the row with the matching ID by getting the columns parent row
        rows.find('td').each(function() {
            id = ($(this).html()).trim();
            if (id == variableId) {
                row = $(this).parent();
            }
        });

        // For each column in the row, push each column into an array
        row.find('td').each(function() {
            data.push($(this).html().trim());
        });

        // Set the inputs values to whats in the array
        $("#id_input").val(data[0]);
        $("#reason_input").val(data[1]);
        $("#content_input").val(data[2]);

        // Edit table data when the okay button is pressed
        $("#modal_okay_button").click(function(event){
            // Get input values
            theReason = $('#reason_input').val();
            theContent = $('#content_input').val();

            // For each column in the row change the HTML to the input field text
            // The count is so we know which column in the row we are at, there might be a nicer way?
            count = 0;

            row.find('td').each(function() {
                // Reason column
                if (count == 1) {
                  $(this).html(theReason);
                }
                // Content column
                else if (count == 2){
                    $(this).html(theContent);
                }
                count ++;
        });
        // Fade out 500ms
        modal.fadeOut(500);
        });

        // Make sure the page doesn't refresh/change when this button is clicked
        return false;
    });
});

