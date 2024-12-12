# -*- coding: utf-8 -*-
# from odoo import http


# class DraftPublish(http.Controller):
#     @http.route('/draft_publish/draft_publish', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/draft_publish/draft_publish/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('draft_publish.listing', {
#             'root': '/draft_publish/draft_publish',
#             'objects': http.request.env['draft_publish.draft_publish'].search([]),
#         })

#     @http.route('/draft_publish/draft_publish/objects/<model("draft_publish.draft_publish"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('draft_publish.object', {
#             'object': obj
#         })

