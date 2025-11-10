# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import xmlrpc.client
import json
import logging
_logger = logging.getLogger(__name__)
# url = "http://localhost:8069"
# db = 'my_co'
url = "http://185.209.229.33:8024"
db = 'asset_16'
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


# uid = common.authenticate(db, username, password, {})
# models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])


class Asset(http.Controller):

    def decrypt_password(self, password):
        # key = "nsHhkPbOUf1CfDfvqKzyxcri6eIi3FOKxQFu_lpY4xw="
        # # Instance the Fernet class with the key
        # fernet = Fernet(key)
        # password = fernet.decrypt(password).decode()
        return [password]

    @http.route('/asset/create_session', type='json', auth='public')
    def asset_create_session(self, **kw):
        data = json.loads(request.httprequest.data)
        username = data.get('username')
        password = data.get('password')
        # password = str.encode(password)
        # password = self.decrypt_password(password)
        # password = password and password[0]
        _logger.info("=========status_update==========", username, password)
        print("=========username, password=======", username, password)
        uid = common.authenticate(db, username, password, {})
        print("=========UID=======",uid)
        if uid:
            try:
                res = models.execute_kw(db, uid, password, 'res.users', 'create_session_and_send_group',
                                        [[uid], username, password])
                return {'success': True,
                        'comments': 'Successful!',
                        'data': res}
            except Exception as e:
                return {'success': False,
                        'message': str(e)}
        else:
            return {'success': False,
                    'message': 'Access Denied/user not found.'}

    @http.route('/asset/order/order_info/<int:order_id>', type='json', auth='public')
    def asset_order_detail(self, order_id, **kw):
        data = json.loads(request.httprequest.data)
        username = data.get('username')
        password = data.get('password')
        # password = str.encode(password)
        # password = self.decrypt_password(password)
        # password = password and password[0]
        session = data.get('session')
        # validate_session_tinmac
        uid = common.authenticate(db, username, password, {})
        try:
            res = models.execute_kw(db, uid, password, 'order.order', 'get_order_details', [[order_id], session])

            return {'success': True,
                    'comments': 'Successful!',
                    'orders': res}
        except Exception as e:
            return {'success': False,
                    'message': str(e)}

    @http.route('/order/order_master_list', type='json', auth='public')
    def order_master(self, **kw):
        """
        This controller will return list of order_master_list data.
        :param kw: Pass extra params
        :return: Dict of equipment data.
        """
        data = json.loads(request.httprequest.data)
        username = data.get('username')
        password = data.get('password')
        # password = str.encode(password)
        # password = self.decrypt_password(password)
        # password = password and password[0]
        uid = common.authenticate(db, username, password, {})
        session = data.get('session')
        message = models.execute_kw(db, uid, password, 'res.users', 'validate_session_tinmac_messsage',
                                    [[uid], session])
        if message and message[0] != 'Okay':
            return {'success': False,
                    'message': str(message[0])}
        try:
            # res = models.execute_kw(db, uid, password, 'order.order', 'search_read',
            #                          [], {'fields': ['id', 'name', 'order_datetime', 'state', 'reason']})
            # res = models.execute_kw(db, uid, password, 'order.order', 'search_read',
            #                         [])
            domain = []
            order = 'order_datetime desc'

            res = models.execute_kw(db, uid, password, 'order.order', 'search_read',
                                    [domain], {'order': order})
            return {
                'success': True,
                'comments': 'Successful!',
                'order_master_list': res,
            }
        except Exception as e:
            return {'success': False,
                    'message': str(e)}

    @http.route('/asset/asset_master_list', type='json', auth='public')
    def asset_master(self, **kw):
        """
        This controller will return list of asset_master_list data.
        :param kw: Pass extra params
        :return: Dict of equipment data.
        """
        data = json.loads(request.httprequest.data)
        username = data.get('username')
        password = data.get('password')
        # password = str.encode(password)
        # password = self.decrypt_password(password)
        # password = password and password[0]
        uid = common.authenticate(db, username, password, {})
        session = data.get('session')
        message = models.execute_kw(db, uid, password, 'res.users', 'validate_session_tinmac_messsage',
                                    [[uid], session])
        if message and message[0] != 'Okay':
            return {'success': False,
                    'message': str(message[0])}
        try:
            # res = models.execute_kw(db, uid, password, 'asset.management', 'search_read',
            #                          [], {'fields': ['id', 'name', 'asset_code', 'asset_category_id', 'barcode', 'tag', 'asset_code_new', 'inventory_count', 'work_center_id']})
            res = models.execute_kw(db, uid, password, 'asset.management', 'search_read', [])
            return {
                'success': True,
                'comments': 'Successful!',
                'asset_master_list': res,
            }
        except Exception as e:
            return {'success': False,
                    'message': str(e)}

    @http.route("/asset/order/orderline_info/<int:line_rec>/<string:state>", type='json', auth='public')
    def asset_line_start_end(self, line_rec, state, **kw):
        data = json.loads(request.httprequest.data)
        username = data.get('username')
        password = data.get('password')
        # password = str.encode(password)
        # password = self.decrypt_password(password)
        # password = password and password[0]
        uid = common.authenticate(db, username, password, {})
        session = data.get('session')
        message = models.execute_kw(db, uid, password, 'res.users', 'validate_session_tinmac_messsage',
                                    [[uid], session])
        if message and message[0] != 'Okay':
            return {'success': False,
                    'message': str(message[0])}
        try:
            if state == 'assign':
                asset_id = models.execute_kw(db, uid, password, 'asset.order.line',
                                             'read', [line_rec], {'fields': ['asset_id']})
                if asset_id:
                    print("ds::", asset_id)
                    order_id = asset_id[0]['id']
                    print("order_id::", order_id)
                    asset_id = asset_id[0]
                    asset_id = asset_id.get('asset_id')

                if asset_id:
                    asset_id = asset_id[0]
                    order_id = asset_id[0]['id']
                    print('ass::', asset_id)
                res = models.execute_kw(db, uid, password, 'order.order', 'action_start', [order_id])
                print(res)
                return {'success': True,
                        'comments': 'Successful!',
                        'order_line': {'id': line_rec,}
                        }
            if state == 'inprogress':
                asset_id = models.execute_kw(db, uid, password, 'asset.order.line',
                                             'read', [line_rec], {'fields': ['asset_id']})
                if asset_id:
                    asset_id = asset_id[0]
                asset_id = asset_id.get('asset_id')
                if asset_id:
                    asset_id = asset_id[0]
                res = models.execute_kw(db, uid, password, 'order.order', 'action_validate', [asset_id])
                return {'success': True,
                        'comments': 'Successful!',
                        'order_line': {'id': line_rec,
                                       }
                        }
        except Exception as e:
            return {'success': False,
                    'message': str(e)}

    # @http.route("/order/status_update/<int:order_id>/<string:state>", type='json', auth='public')
    # def asset_line_start_end(self, order_id, state, **kw):
    #     data = json.loads(request.httprequest.data)
    #     username = data.get('username')
    #     password = data.get('password')
    #     _logger.info("=========status_update==========", username, password)
    #     uid = common.authenticate(db, username, password, {})
    #     session = data.get('session')
    #     message = models.execute_kw(db, uid, password, 'res.users', 'validate_session_tinmac_messsage',
    #                                 [[uid], session])
    #     if message and message[0] != 'Okay':
    #         return {'success': False,
    #                 'message': str(message[0])}
    #     try:
    #         if state == 'assign':
    #             Is_order_id = models.execute_kw(db, uid, password, 'order.order', 'search', [[['id', '=', order_id]]],
    #                                             {'context': {'session': session}})
    #             if Is_order_id:
    #                 main_oder_id = Is_order_id[0]
    #                 res = models.execute_kw(db, uid, password, 'order.order', 'action_start', [main_oder_id])
    #                 return {'success': True,
    #                         'comments': 'Successful!',
    #                         'order_line': {'id': order_id}}
    #             else:
    #                 return {'success': False,
    #                         'comments': 'ID not present or check with your ID',
    #                         'order_line': {'id': order_id}}
    #
    #         if state == 'inprogress':
    #             _logger.info("=========================")
    #             Is_order_id = models.execute_kw(db, uid, password, 'order.order', 'search', [[['id', '=', order_id]]],
    #                                             {'context': {'session': session}})
    #             if Is_order_id:
    #                 _logger.info("========22222=============",Is_order_id)
    #                 main_oder_id = Is_order_id[0]
    #                 res = models.execute_kw(db, uid, password, 'order.order', 'api_action_validate', [main_oder_id])
    #                 return {'success': True,
    #                         'comments': 'Successful!',
    #                         'order_line': {'id': order_id}}
    #             else:
    #                 return {'success': False,
    #                         'comments': 'ID not present or check with your ID',
    #                         'order_line': {'id': order_id}}
    #     except Exception as e:
    #         return {'success': False,
    #                 'message': str(e)}

    @http.route("/order/status_update/<int:order_id>/<string:state>", type='json', auth='public')
    def asset_line_start_end(self, order_id, state, **kw):
        data = json.loads(request.httprequest.data)
        username = data.get('username')
        password = data.get('password')
        uid = common.authenticate(db, username, password, {})
        session = data.get('session')
        message = models.execute_kw(db, uid, password, 'res.users', 'validate_session_tinmac_messsage',
                                    [[uid], session])
        if message and message[0] != 'Okay':
            return {'success': False,
                    'message': str(message[0])}
        try:
            if state == 'assign':
                Is_order_id = models.execute_kw(db, uid, password, 'order.order', 'search', [[['id', '=', order_id]]],
                                                {'context': {'session': session}})
                if Is_order_id:
                    main_oder_id = Is_order_id[0]
                    res = models.execute_kw(db, uid, password, 'order.order', 'action_start', [main_oder_id])
                    return {'success': True,
                            'comments': 'Successful!',
                            'order_line': {'id': order_id}}
                else:
                    return {'success': False,
                            'comments': 'ID not present or check with your ID',
                            'order_line': {'id': order_id}}

            if state == 'inprogress':
                Is_order_id = models.execute_kw(db, uid, password, 'order.order', 'search', [[['id', '=', order_id]]],
                                                {'context': {'session': session}})
                if Is_order_id:
                    main_oder_id = Is_order_id[0]
                    res = models.execute_kw(db, uid, password, 'order.order', 'api_action_validate', [main_oder_id])
                    return {'success': True,
                            'comments': 'Successful!',
                            'order_line': {'id': order_id}}
                else:
                    return {'success': False,
                            'comments': 'ID not present or check with your ID',
                            'order_line': {'id': order_id}}
        except Exception as e:
            return {'success': False,
                    'message': str(e)}

    @http.route("/asset/order/line/<int:line_id>", type='json', auth='public')
    def asset_order_line_save(self, line_id, **kw):
        # asset.order.line
        data = json.loads(request.httprequest.data)
        update_data = data.get('update_data')
        username = data.get('username')
        password = data.get('password')
        # password = str.encode(password)
        # password = self.decrypt_password(password)
        # password = password and password[0]
        uid = common.authenticate(db, username, password, {})
        session = data.get('session')
        message = models.execute_kw(db, uid, password, 'res.users', 'validate_session_tinmac_messsage',
                                    [[uid], session])
        if message and message[0] != 'Okay':
            print('22222')
            return {'success': False,
                    'message': str(message[0])}
        if uid:
            if line_id:
                try:
                    line_found = models.execute_kw(db, uid, password, 'asset.order.line',
                                                   'read', [line_id], {'fields': ['asset_id']})
                    if not line_found:
                        return {'success': False,
                                'message': 'Order Line Id is missing.'}
                    models.execute_kw(db, uid, password, 'asset.order.line', 'write', [[line_id], update_data])
                    return {'success': True,
                            'line_id': line_id,
                            'message': "Order Line is updated."}
                except Exception as e:
                    return {'success': False,
                            'message': str(e)}
            else:
                return {'success': False,
                        'message': 'Order Line Id is missing.'}
        else:
            return {'success': False,
                    'message': 'Access Denied/user not found.'}

    @http.route("/asset/order/update/lines", type='json', auth='public')
    def asset_order_line_save(self, **kw):
        # asset.order.line
        data = json.loads(request.httprequest.data)
        update_data = data.get('order_updates')
        # print("update_data:::", update_data)
        username = data.get('username')
        password = data.get('password')
        _logger.info("****Order Line Update***",username, password, data)
        # password = str.encode(password)
        # password = self.decrypt_password(password)
        # password = password and password[0]
        uid = common.authenticate(db, username, password, {})
        session = data.get('session')
        message = models.execute_kw(db, uid, password, 'res.users', 'validate_session_tinmac_messsage',
                                    [[uid], session])
        if message and message[0] != 'Okay':
            return {'success': False,
                    'message': str(message[0])}
        if uid:
            order_lines = []
            for asset_line in update_data:
                line_id = asset_line['line_id']
                if line_id:
                    try:
                        line_found = models.execute_kw(db, uid, password, 'asset.order.line',
                                                       'read', [line_id], {'fields': ['asset_id']})
                        if not line_found:
                            order_lines.append({'success': False,
                                                'line_id': line_id,
                                                'message': "Order Line Id is missing."})
                        else:
                            del asset_line['line_id']
                            models.execute_kw(db, uid, password, 'asset.order.line', 'write', [[line_id], asset_line])
                            order_lines.append({'success': True,
                                                'line_id': line_id,
                                                'message': "Order Lines is updated."})

                    except Exception as e:
                        return {'success': False,
                                'message': str(e)}
                else:
                    order_lines.append({'success': False,
                                        'line_id': line_id,
                                        'message': "Order Line Id is missing."})
            # print(order_lines,"order_lines")
            return order_lines
        else:
            return {'success': False,
                    'message': 'Access Denied/user not found.'}

    @http.route("/asset/update/<int:asset_id>", type='json', auth='public')
    def asset_update(self, asset_id, **kw):
        # asset.management
        data = json.loads(request.httprequest.data)
        update_data = data.get('update_data')
        username = data.get('username')
        password = data.get('password')
        # password = str.encode(password)
        # password = self.decrypt_password(password)
        # password = password and password[0]
        uid = common.authenticate(db, username, password, {})
        session = data.get('session')
        message = models.execute_kw(db, uid, password, 'res.users', 'validate_session_tinmac_messsage',
                                    [[uid], session])
        if message and message[0] != 'Okay':
            return {'success': False,
                    'message': str(message[0])}
        if asset_id:
            try:
                asset_found = models.execute_kw(db, uid, password, 'asset.management',
                                                'read', [asset_id], {'fields': ['name']})
                if not asset_found:
                    return {'success': False,
                            'message': 'Asset Line Id is missing.'}
                models.execute_kw(db, uid, password, 'asset.management', 'write', [[asset_id], update_data])
                return {'success': True,
                        'line_id': asset_id,
                        'message': "Asset Line is updated."}
            except Exception as e:
                return {'success': False,
                        'message': str(e)}
        return {'success': False,
                'message': 'Asset Line Id is missing.'}

    @http.route('/order/order_master_list_old', type='json', auth='public')
    def order_master_old(self, **kw):
        """
        This controller will return list of order_master_list data.
        :param kw: Pass extra params
        :return: Dict of equipment data.
        """
        data = json.loads(request.httprequest.data)
        username = data.get('username')
        password = data.get('password')
        # password = str.encode(password)
        # password = self.decrypt_password(password)
        # password = password and password[0]
        uid = common.authenticate(db, username, password, {})
        session = data.get('session')
        message = models.execute_kw(db, uid, password, 'res.users', 'validate_session_tinmac_messsage',
                                    [[uid], session])
        if message and message[0] != 'Okay':
            return {'success': False,
                    'message': str(message[0])}
        try:
            # res = models.execute_kw(db, uid, password, 'order.order', 'search_read',
            #                          [], {'fields': ['id', 'name', 'order_datetime', 'state', 'reason']})
            res = models.execute_kw(db, uid, password, 'order.order', 'search_read',
                                    [])

            return {
                'success': True,
                'comments': 'Successful!',
                'order_master_list': res,
            }
        except Exception as e:
            return {'success': False,
                    'message': str(e)}
