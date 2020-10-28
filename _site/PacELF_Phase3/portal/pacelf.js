document.body.addEventListener('portalPageRendered', function(e) {

  setTimeout(function() {
    //Hide all Download buttons wherer the 'Access Rights' are not 'Open'
    // (changing this coz there's now a text doc saying "contact ")
    // $("h3.mf-metadata-field:contains('Access Rights')").siblings(".mf-metadata-value:not(:contains('Open'))").parent().parent().parent().parent().siblings("button.mf-download-button").hide()

    //Convert all 'View at Publisher' values to html links.
    $("h3.mf-metadata-field:contains('View at Publisher')").siblings(".mf-metadata-value").replaceWith(function() {
      return "<div class='mf-metadata-value'><a href='" + $(this).text() + "' target='_blank' >" + $(this).text() + "</a></div>";
    });

    //Limit the height and add scroll bars for Description metadata.
    $("h3.mf-metadata-field:contains('Description')").siblings(".mf-metadata-value").replaceWith(function() {
      return "<div class='mf-metadata-value'><p style='max-height: 200px; overflow-y: auto; overflow-x: hidden;'>" + $(this).text() + "</p></div>";
    });

    //Show Flag image for the Work Location where possible
    $("h3.mf-metadata-field:contains('Work Location')").siblings(".mf-metadata-value").each(function(index, element) {

      var flags = [
        "American Samoa",
        "Australia",
        "Cook Islands",
        "Fiji",
        "French Polynesia",
        "Federated States of Micronesia",
        "Guam",
        "Japan",
        "Kiribati",
        "Marshall Islands",
        "Nauru",
        "New Caledonia",
        "New Zealand",
        "Niue",
        "Northern Mariana",
        "Palau",
        "Papua New Guinea",
        "Pitcairn Islands",
        "Samoa",
        "Solomon Islands",
        "Tokelau",
        "Tonga",
        "Tuvalu",
        "Vanuatu",
        "Wallis and Futuna"
      ]

      if (flags.indexOf($(this).text()) != -1) {
        // $(this).closest(".mf-listed-result").find(".mf-result-thumbnail-wrapper").after($("<img class='flags' src='/resources/pacelf2/flags/" + $(this).text() + ".svg' alt='" + $(this).text() + "' />"));
      }
    });

  }, 0);

}, false);


//Get all text from the h3, mf-metadata-field and contains the value 'Access Rights'
//$("h3.mf-metadata-field:contains('Access Rights')").text()

//now get the value of the sibling containing the class mf-metadata-value
//$("h3.mf-metadata-field:contains('Access Rights')").siblings(".mf-metadata-value").text()

//now does not contain 'Open'
//$("h3.mf-metadata-field:contains('Access Rights')").siblings(".mf-metadata-value:not(:contains('Open'))").text()

//now find the buttons and hide them
//$("button.mf-download-button").hide();

//This works, now to make is nice, its ugly code.
//$("h3.mf-metadata-field:contains('Access Rights')").siblings(".mf-metadata-value:not(:contains('Open'))").parent().parent().parent().parent().siblings("button.mf-download-button").hide()

//Convert to anchor links, this works
//$("h3.mf-metadata-field:contains('View at Publisher')").siblings(".mf-metadata-value").replaceWith(function() {
//  return "<a href='" + $(this).text() + "'>" + $(this).text() + "</a>";
//});
