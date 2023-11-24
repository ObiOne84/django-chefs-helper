// update html page date
$('#copyright').text(new Date().getFullYear());

// print recipe card
$('#print-button').on("click", function () {
    let body = $('body').html();
    print(body);
});