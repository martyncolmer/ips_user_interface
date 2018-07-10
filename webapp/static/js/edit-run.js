/*
    Created by Jack Allcock 21/06/2018
    This javascript file handles the edit PV's modal
*/

$(document).ready(function(e){

    // Create dictionary of all the table cell rows
    var tableRows = [];
            $("#form_table > tbody  > tr").each(function() {
                var row = {
                  "name" : $(this).find(".table--cell")[0],
                  "reason" : $(this).find(".table--cell")[1],
                  "content" : $(this).find(".table--cell")[2],
                };
                tableRows.push(row);
            });

    // Create dictionary of all the inputs
    var tableInputs = [];
           $(".hidden-edit-inputs").each(function() {
               var row = {
                 "name" : $(this).find(".hidden-edit-input-name"),
                 "reason" : $(this).find(".hidden-edit-input-reason"),
                 "content" : $(this).find(".hidden-edit-input-content"),
               };
               tableInputs.push(row);
           });

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

        // Length of the rows in the table
        rowsLength = tableRows.length
        // Array we will append rows to
        data = [];

        /** First we need to go through the table data and find the row we need.
            Then we can set the modal inputs with data from that table row and update the actual table data when the
            okay button is clicked
        **/

        // Iterate over dictionary of table rows
        for (i=0; i < rowsLength; i++) {
            // Get dictionary out of array by index
            row = tableRows[i];
            // Get the PV Name text
            name = row['name'].innerHTML;

            // If the dictionary is the one we need add the data to the array
            if (name === variableId) {
                data.push(row['name']);
                data.push(row['reason']);
                data.push(row['content']);
            }
        }

        // Set the inputs values to that in the data array
        $("#id_input").val(data[0].innerHTML);
        $("#reason_input").val(data[1].innerHTML);
        $("#content_input").val(data[2].innerHTML);

        // Edit table data when the okay button is pressed
        $("#modal_okay_button").click(function(event){
            // Get values entered into the inputs by the user
            reasonInput = $('#reason_input').val();
            contentInput = $('#content_input').val();

            // Get the data from data array
            reason = data[1];
            content = data[2];

            // Update the table data to that in the array
            reason.innerHTML = reasonInput;
            content.innerHTML = contentInput;

            /** Now we need to go through the inputs in the table to get the ones we need.
                We can update them with the new input values to post to Flask.
            **/

            // Iterate over dictionary of inputs
            for (i=0; i < rowsLength; i++) {
                // Get dictionary out of array by index
                row = tableInputs[i];
                // Get the PV Name text
                name = row['name'].val();

                // If the dictionary is the one we need add the data to the array
                if (name === variableId) {
                    // Update the input fields in the table with the ones the user entered
                    row['reason'].val(reasonInput);
                    row['content'].val(contentInput);
                }
            }

        // Fade out 500ms
        modal.fadeOut(500);
        });

        // Make sure the page doesn't refresh/change when this button is clicked
        return false;
    });
});

