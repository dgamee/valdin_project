$(document).ready(function(){

    // Function to get CSRF token from cookies
    const csrftoken = document.cookie.split('=')[1];
    // Delete product from cart
    $("#delete-product").on("click", function(){
        let product_id = $(this).attr('data-product');
        let url = `cart/${product_id}/delete/`;
        let this_val = $(this);

        $.ajax({
            url: url,
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data : {
                'product_id' : product_id
            },
            dataType : 'json',
            beforeSend: function(){
                this_val.hide();
            },
            success: function(response){
                if (response.success) {
                    this_val.closest('.card').remove();
                    $('.cart-items-count').text(response.totalcartitems);
                    location.reload()
                } else {
                    alert(response.error);
                    this_val.prop('disabled', false);
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = xhr.responseJSON.error;
                console.error('Error deleting product:', errorMessage);
                alert(errorMessage);
                this_val.prop('disabled', false);
            }
        });
    });

    // Update quantity
    $(".update-quantity").on("click", function(){
        let product_id = $(this).data('product-id');
        let new_quantity = $("#quantity-" + product_id).val();

        $.ajax({
            url: window.location.href,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken  // Pass CSRF token in headers
            },
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'update_quantity',
                'product_id': product_id,
                'new_quantity': new_quantity
            },
            beforeSend: function(){
                // Hide elements or show loading indicator if needed
            },
            success: function(response) {
                if(response.message) {
                    location.reload();  // Reload page after successful update
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = xhr.responseJSON.error;
                console.error('Error updating quantity:', errorMessage);
                location.reload();  // Display error to user
            }
        });
    });

    // Checkout
    $(".checkout").on("click", function(){
        $.ajax({
            url: window.location.href,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken  // Pass CSRF token in headers
            },
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'checkout'
            },
            success: function(response) {
                if(response.message) {
                    location.reload();  // Reload page after successful checkout
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = xhr.responseJSON.error;
                console.error('Error during checkout:', errorMessage);
                alert(errorMessage);  // Display error to user
            }
        });
    });

});
