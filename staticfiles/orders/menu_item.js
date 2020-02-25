window.addEventListener('DOMContentLoaded', function() {
  
	var limit = JSON.parse(document.getElementById('toppings-data').textContent);
  var checkedcount = 0;

  document.querySelectorAll('.toppings_checkbox').forEach(function(checkbox){

      checkbox.onchange = function() {

        if (checkbox.checked == true){
          checkedcount += 1;
        } else{
          checkedcount -= 1;
        }
        if (checkedcount === limit){
          document.querySelectorAll('.toppings_checkbox').forEach(function(checkbox){
            if (checkbox.checked == false){
              checkbox.disabled = true;
            }
          });
        }else{
          document.querySelectorAll('.toppings_checkbox').forEach(function(checkbox){
            checkbox.disabled = false;
          });
        }
      };
  });



});
