import pytest, requests
U, R = "http://localhost:8080/api/v1", "2024111006"
def q(m, p, j=None, h=None):
    if h is None: h = {"X-Roll-Number": R, "X-User-ID": "1"}
    return requests.request(m, f"{U}{p}", json=j, headers=h)

# --- HEADERS ---
def test_h_miss_roll(): assert q('GET','/admin/users',h={}).status_code == 401
def test_h_alpha_roll(): assert q('GET','/admin/users',h={"X-Roll-Number":"ABC"}).status_code == 400
def test_h_neg_roll(): assert q('GET','/admin/users',h={"X-Roll-Number":"-1"}).status_code == 401
def test_h_zero_roll(): assert q('GET','/admin/users',h={"X-Roll-Number":"0"}).status_code == 401
def test_h_miss_uid(): assert q('GET','/profile',h={"X-Roll-Number":R}).status_code == 400
def test_h_non_int_uid(): assert q('GET','/profile',h={"X-Roll-Number":R,"X-User-ID":"ABC"}).status_code == 400
def test_h_neg_uid(): assert q('GET','/profile',h={"X-Roll-Number":R,"X-User-ID":"-1"}).status_code == 400
def test_h_zero_uid(): assert q('GET','/profile',h={"X-Roll-Number":R,"X-User-ID":"0"}).status_code == 400
def test_h_large_uid(): assert q('GET','/profile',h={"X-Roll-Number":R,"X-User-ID":"999999"}).status_code in [400, 404]
def test_h_valid(): assert q('GET','/admin/users',h={"X-Roll-Number":R}).status_code == 200
def test_h_valid_all(): assert q('GET', '/profile', h={"X-Roll-Number":R, "X-User-ID":"1"}).status_code == 200
def test_h_long_roll(): assert q('GET','/admin/users',h={"X-Roll-Number":"1"*20}).status_code == 401
def test_h_float_uid(): assert q('GET','/profile',h={"X-Roll-Number":R,"X-User-ID":"1.5"}).status_code == 400
def test_h_wrong_key(): assert q('GET','/admin/users',h={"Roll":R}).status_code == 401

# --- ADMIN ---
def test_adm_users(): assert q('GET','/admin/users').status_code == 200
def test_adm_user_1(): assert q('GET','/admin/users/1').status_code == 200
def test_adm_carts(): assert q('GET','/admin/carts').status_code == 200
def test_adm_orders(): assert q('GET','/admin/orders').status_code == 200
def test_adm_products(): assert q('GET', '/admin/products').status_code == 200
def test_adm_coupons(): assert q('GET', '/admin/coupons').status_code == 200
def test_adm_tickets(): assert q('GET', '/admin/tickets').status_code == 200
def test_adm_addresses(): assert q('GET', '/admin/addresses').status_code == 200
def test_adm_user_non(): assert q('GET', '/admin/users/999').status_code == 404
def test_adm_user_neg(): assert q('GET', '/admin/users/-1').status_code == 400

# --- PROFILE ---
def test_p_get(): assert q('GET','/profile').status_code == 200
def test_p_upd_valid(): assert q('PUT','/profile',{"name":"Valid","phone":"1234567890"}).status_code == 200
def test_p_upd_short_n(): assert q('PUT','/profile',{"name":"A","phone":"1234567890"}).status_code == 400
def test_p_upd_long_n(): assert q('PUT','/profile',{"name":"A"*51,"phone":"1234567890"}).status_code == 400
def test_p_upd_short_p(): assert q('PUT','/profile',{"name":"Name","phone":"123456789"}).status_code == 400
def test_p_upd_long_p(): assert q('PUT','/profile',{"name":"Name","phone":"12345678901"}).status_code == 400
def test_p_upd_alpha_p(): assert q('PUT','/profile',{"name":"Name","phone":"ABCDEFGHIJ"}).status_code == 400
def test_p_upd_empty(): assert q('PUT','/profile',{}).status_code == 400
def test_p_upd_miss_n(): assert q('PUT','/profile',{"phone":"1234567890"}).status_code == 400
def test_p_upd_miss_p(): assert q('PUT','/profile',{"name":"Name"}).status_code == 400
def test_p_upd_num_n(): assert q('PUT','/profile',{"name":123,"phone":"1234567890"}).status_code == 400
def test_p_upd_nul_n(): assert q('PUT','/profile',{"name":None,"phone":"1234567890"}).status_code == 400
def test_p_upd_nul_p(): assert q('PUT','/profile',{"name":"Valid","phone":None}).status_code == 400
def test_p_upd_sym_n(): assert q('PUT','/profile',{"name":"Valid!","phone":"1234567890"}).status_code == 200
def test_p_upd_hyph_p(): assert q('PUT','/profile',{"name":"Valid","phone":"123-456-78"}).status_code == 400

# --- ADDRESSES ---
def test_a_get(): assert q('GET','/addresses').status_code == 200
def test_a_add_home(): assert q('POST','/addresses',{"label":"HOME","street":"ValidSt","city":"City","pincode":"123456"}).status_code == 200
def test_a_add_off(): assert q('POST','/addresses',{"label":"OFFICE","street":"ValidSt","city":"City","pincode":"123456"}).status_code == 200
def test_a_add_oth(): assert q('POST','/addresses',{"label":"OTHER","street":"ValidSt","city":"City","pincode":"123456"}).status_code == 200
def test_a_add_wrong_lab(): assert q('POST','/addresses',{"label":"FAKE","street":"ValidSt","city":"City","pincode":"123456"}).status_code == 400
def test_a_add_short_st(): assert q('POST','/addresses',{"label":"HOME","street":"A","city":"City","pincode":"123456"}).status_code == 400
def test_a_add_short_ci(): assert q('POST','/addresses',{"label":"HOME","street":"ValidSt","city":"A","pincode":"123456"}).status_code == 400
def test_a_add_short_pi(): assert q('POST','/addresses',{"label":"HOME","street":"ValidSt","city":"City","pincode":"12345"}).status_code == 400
def test_a_add_long_pi(): assert q('POST','/addresses',{"label":"HOME","street":"ValidSt","city":"City","pincode":"1234567"}).status_code == 400
def test_a_add_alpha_pi(): assert q('POST','/addresses',{"label":"HOME","street":"ValidSt","city":"City","pincode":"ABCDEF"}).status_code == 400
def test_a_add_empty(): assert q('POST','/addresses',{}).status_code == 400
def test_a_upd_st(): assert q('PUT','/addresses/1',{"street":"New Street"}).status_code == 200
def test_a_upd_def(): assert q('PUT','/addresses/1',{"is_default":True}).status_code == 200
def test_a_upd_non(): assert q('PUT','/addresses/999',{"street":"New"}).status_code == 404
def test_a_upd_label(): assert q('PUT','/addresses/1',{"label":"OFFICE"}).status_code == 400
def test_a_up_wrong_bool(): assert q('PUT','/addresses/1',{"is_default":"X"}).status_code == 400
def test_a_add_num_ci(): assert q('POST','/addresses',{"label":"HOME","street":"Str","city":123,"pincode":"111111"}).status_code == 400
def test_a_logic_multi_def():
    q('POST','/addresses',{"label":"HOME","street":"Str1","city":"C","pincode":"111111","is_default":True})
    q('POST','/addresses',{"label":"HOME","street":"Str2","city":"C","pincode":"111111","is_default":True})
    defs = [a for a in q('GET','/addresses').json() if a.get("is_default")]
    assert len(defs) <= 1
def test_a_add_low_label(): assert q('POST','/addresses',{"label":"home","street":"Valid","city":"City","pincode":"123456"}).status_code == 400

# --- PRODUCTS ---
def test_pro_list(): assert q('GET','/products').status_code == 200
def test_pro_get_1(): assert q('GET','/products/1').status_code == 200
def test_pro_get_non(): assert q('GET','/products/999').status_code == 404
def test_pro_filter_cat(): assert q('GET','/products?category=Electronics').status_code == 200
def test_pro_search(): assert q('GET','/products?name=Phone').status_code == 200
def test_pro_sort_asc(): assert q('GET','/products?sort=price&order=asc').status_code == 200
def test_pro_sort_desc():
    p = q('GET','/products?sort=price&order=desc').json()
    if len(p) > 1: assert p[0]['price'] >= p[1]['price']
def test_pro_search_empty(): assert len(q('GET','/products?name=ZZZZZZ').json()) == 0
def test_pro_neg_id(): assert q('GET','/products/-1').status_code == 400
def test_pro_alpha_id(): assert q('GET','/products/ABC').status_code == 400
def test_pro_price_match():
    p1 = q('GET','/products/1').json()
    p_all = q('GET','/admin/products').json()
    p_adm = next(x for x in p_all if x['product_id']==1)
    assert p1['price'] == p_adm['price']

# --- CART ---
def test_c_get(): assert q('GET','/cart').status_code == 200
def test_c_add_valid(): assert q('POST','/cart/add',{"product_id":1,"quantity":1}).status_code == 200
def test_c_add_zero(): assert q('POST','/cart/add',{"product_id":1,"quantity":0}).status_code == 400
def test_c_add_neg(): assert q('POST','/cart/add',{"product_id":1,"quantity":-1}).status_code == 400
def test_c_add_non(): assert q('POST','/cart/add',{"product_id":999,"quantity":1}).status_code == 404
def test_c_upd_valid():
    q('POST','/cart/add',{"product_id":1,"quantity":1})
    assert q('POST','/cart/update',{"product_id":1,"quantity":2}).status_code == 200
def test_c_upd_zero(): assert q('POST','/cart/update',{"product_id":1,"quantity":0}).status_code == 400
def test_c_rem_valid():
    q('POST','/cart/add',{"product_id":1,"quantity":1})
    assert q('POST','/cart/remove',{"product_id":1}).status_code == 200
def test_c_rem_non(): assert q('POST','/cart/remove',{"product_id":999}).status_code == 404
def test_c_clear(): assert q('DELETE','/cart/clear').status_code == 200
def test_c_add_stack():
    q('DELETE','/cart/clear'); q('POST','/cart/add',{"product_id":1,"quantity":1}); q('POST','/cart/add',{"product_id":1,"quantity":1})
    item = next(x for x in q('GET','/cart').json()['items'] if x['product_id']==1)
    assert item['quantity'] == 2
def test_c_subtotal():
    q('DELETE','/cart/clear'); q('POST','/cart/add',{"product_id":1,"quantity":2})
    it = q('GET','/cart').json()['items'][0]
    assert it['subtotal'] == it['quantity'] * it.get('price', 0)
def test_c_total():
    q('DELETE','/cart/clear'); q('POST','/cart/add',{"product_id":1,"quantity":1}); q('POST','/cart/add',{"product_id":2,"quantity":1})
    c = q('GET','/cart').json()
    assert c['total'] == sum(x['subtotal'] for x in c['items'])
def test_c_math_bug():
    q('DELETE','/cart/clear'); q('POST','/cart/add',{"product_id":1,"quantity":2})
    assert q('GET','/cart').json()['total'] > 0
def test_c_up_non_cart():
    q('DELETE','/cart/clear')
    assert q('POST','/cart/update',{"product_id":2,"quantity":5}).status_code == 404
def test_c_add_miss_id(): assert q('POST','/cart/add',{"quantity":1}).status_code == 400
def test_c_add_miss_q(): assert q('POST','/cart/add',{"product_id":1}).status_code == 400

# --- COUPONS ---
def test_cp_apply_mega15(): assert q('POST','/coupon/apply',{"coupon_code":"MEGA15"}).status_code in [200, 400]
def test_cp_apply_fake(): assert q('POST','/coupon/apply',{"coupon_code":"FAKE"}).status_code == 404
def test_cp_apply_empty(): assert q('POST','/coupon/apply',{"coupon_code":""}).status_code == 400
def test_cp_rem_valid(): assert q('POST','/coupon/remove').status_code == 200
def test_cp_apply_case(): assert q('POST','/coupon/apply',{"coupon_code":"mega15"}).status_code == 404
def test_cp_apply_space(): assert q('POST','/coupon/apply',{"coupon_code":"MEGA 15"}).status_code == 404

# --- CHECKOUT ---
def test_chk_card():
    q('POST','/cart/add',{"product_id":1,"quantity":1})
    assert q('POST','/checkout',{"payment_method":"CARD"}).status_code == 200
def test_chk_empty_cart():
    q('DELETE','/cart/clear')
    assert q('POST','/checkout',{"payment_method":"CARD"}).status_code == 400
def test_chk_cod_limit():
    q('DELETE','/cart/clear'); q('POST','/cart/add',{"product_id":4,"quantity":10})
    assert q('POST','/checkout',{"payment_method":"COD"}).status_code == 400
def test_chk_gst_calc():
    q('DELETE','/cart/clear'); q('POST','/cart/add',{"product_id":1,"quantity":1})
    oid = q('POST','/checkout',{"payment_method":"CARD"}).json()['order_id']
    inv = q('GET',f'/orders/{oid}/invoice').json()
    assert abs(inv.get('gst_amount',0) - inv.get('subtotal',0)*0.05) < 0.1

# --- WALLET ---
def test_w_add_valid(): assert q('POST','/wallet/add',{"amount":100}).status_code == 200
def test_w_add_neg(): assert q('POST','/wallet/add',{"amount":-1}).status_code == 400
def test_w_add_float(): assert q('POST','/wallet/add',{"amount":1.5}).status_code == 400

# --- LOYALTY ---
def test_l_red_valid(): assert q('POST','/loyalty/redeem',{"amount":1}).status_code in [200, 400]
def test_l_get_adm():
    u = q('GET','/admin/users/1').json()
    l = q('GET','/loyalty').json()
    assert u.get('loyalty_points') == l.get('points')

# --- ORDERS ---
def test_o_get_non(): assert q('GET','/orders/9999').status_code == 404
def test_o_inv_fields():
    q('POST','/cart/add',{"product_id":1,"quantity":1})
    oid = q('POST','/checkout',{"payment_method":"CARD"}).json()['order_id']
    inv = q('GET',f'/orders/{oid}/invoice').json()
    assert 'subtotal' in inv and 'total_amount' in inv
def test_o_inv_gst_name():
    q('POST','/cart/add',{"product_id":1,"quantity":1})
    oid = q('POST','/checkout',{"payment_method":"CARD"}).json()['order_id']
    assert 'gst_amount' in q('GET',f'/orders/{oid}/invoice').json()
def test_o_get_alpha(): assert q('GET','/orders/ABC').status_code == 400

# --- REVIEWS ---
def test_rv_get(): assert q('GET','/products/1/reviews').status_code == 200
def test_rv_get_non(): assert q('GET','/products/999/reviews').status_code == 404
def test_rv_avg_calc():
    q('POST','/products/2/reviews',{"rating":5,"comment":"A"})
    q('POST','/products/2/reviews',{"rating":4,"comment":"B"})
    assert 'average_rating' in q('GET','/products/2').json()

# --- TICKETS ---
def test_tk_add_valid(): assert q('POST','/support/ticket',{"subject":"ValidSubject","message":"M"}).status_code == 200
def test_tk_add_vshort_s(): assert q('POST','/support/ticket',{"subject":"Short","message":"M"}).status_code == 400
def test_tk_upd_rollback():
    tid = q('POST','/support/ticket',{"subject":"Subject","message":"M"}).json()['ticket_id']
    q('PUT',f'/support/tickets/{tid}',{"status":"CLOSED"})
    assert q('PUT',f'/support/tickets/{tid}',{"status":"OPEN"}).status_code == 400
def test_tk_upd_invalid_s():
    tid = q('POST','/support/ticket',{"subject":"Subject","message":"M"}).json()['ticket_id']
    assert q('PUT',f'/support/tickets/{tid}',{"status":"FAKE"}).status_code == 400
