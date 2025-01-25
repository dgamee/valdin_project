$("#add-to-cart-btn").on("click", function(){
    let quantity = $("#product-quantity").val();
    let product_name = $(".product-name").val();
    let product_id = $(".product-id").val();
    let product_price = $("#product-price").text();
    let this_val = $(this);

    console.log("quantity: ", quantity);
    console.log("product name: ", product_name);
    console.log("product Id: ", product_id);
    console.log("product price: ", product_price);
    console.log("current element: ", this_val);

    $.ajax({
        url: `add-to-cart/`, // Ensure this URL matches your URL pattern
        data: {
            'id': product_id,
            'quantity': quantity,
            'name': product_name,
            'product_price': product_price,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Adding product to cart...');
        },
        success: function(response){
            this_val.html('Item Added to Cart');
            console.log("Added to cart:", response);
            $('.cart-items-count').text(response.totalcartitems)
            location.reload()
            // Optionally, you can redirect or update UI based on success
        },
        error: function(xhr, status, error) {
            console.error('Error adding to cart:', error);
            let errorMessage = xhr.responseJSON.error;
            location.reload();
            // Handle error cases here
        }
    });
});


