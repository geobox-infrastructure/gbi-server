# This file is part of the GBI project.
# Copyright (C) 2013 Omniscale GmbH & Co. KG <http://omniscale.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from wtforms.fields import TextField, TextAreaField, IntegerField, PasswordField, SelectField, BooleanField, DateField
from wtforms import validators

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext as _l

from user import NewUserForm


class CreateUserForm(NewUserForm):
    type = SelectField(_l('type'), coerce=int)
    verified = BooleanField(_l('verified'), default=False)
    activate = BooleanField(_l('active'), default=False)
    terms_of_use = BooleanField(_l('terms of use'), default=True)


class SearchUserForm(Form):
    name = TextField(_l('firstname or lastname'))
    email = TextField(_l('email'))
    zipcode_or_city = TextField(_l('zipcode or city'))
    federal_state = SelectField(
        _l('federal_state'),
        choices=[] # at the moment choices are set on view, because we load they from config
    )
    type = SelectField(_l('type'), coerce=int)
    company_number = TextField(_l('company_number'),)
    status = SelectField(
        _l('status'),
        choices=[
            ('', ''),
            (True, _l('active')),
            ('False', _l('not active')),
        ]
    )
    access_start = DateField(_l('access_start'), format='%d.%m.%Y')
    access_end = DateField(_l('access_end'), format='%d.%m.%Y')


class SearchForm(Form):
    """
    We expect search queries to come externally, thus we don't want CSRF
    even though it's set up on the base form.
    """
    class Meta:
        # This overrides the value from the base form.
        csrf = False

class DownloadLogsForm(SearchForm):
    access_start = DateField(_l('access_start'), format='%d.%m.%Y %H:%M:%S')
    access_end = DateField(_l('access_end'), format='%d.%m.%Y %H:%M:%S')


class RasterSourceForm(Form):
    url = TextField(_l('rastersource_url'), [validators.Required()])
    username = TextField(_l('rastersource_username'))
    password = PasswordField(_l('rastersource_password'))
    name = TextField(_l('rastersource_name'), [validators.Required(), validators.Regexp('[a-z0-9_-]+$')])
    title = TextField(_l('rastersource_title'), [validators.Required()])
    layer = TextField(_l('rastersource_layer'), [validators.Required()])
    format = SelectField(_l('rastersource_format'), [validators.Required()], choices=[('png', 'png'), ('jpeg', 'jpeg')])
    srs = TextField(_l('rastersource_srs'), [validators.Required()])
    max_tiles = TextField(_l('rastersource_max_tiles'), [validators.Regexp('^\d*$')])

    view_coverage = TextAreaField(_l('rastersource_view_coverage'), [validators.Required()]) #XXX kai: geojson validator?
    view_level_start = SelectField(_l('rastersource_view_level_start'), coerce=int, choices=[(x, x) for x in range(20)])
    view_level_end = SelectField(_l('rastersource_view_level_end'), coerce=int, choices=[(x, x) for x in range(20)])

    is_background_layer = BooleanField(_l('rastersource_background_layer'))
    is_transparent = BooleanField(_l('rastersource_transparent'))
    is_visible = BooleanField(_l('rastersource_visibility'))
    is_public = BooleanField(_l('rastersource_public'))
    is_accessible = BooleanField(_l('rastersource_accessible'))
    is_protected = BooleanField(_l('rastersource_protected'))

    def validate_view_level_end(form, field):
        if form.data['view_level_start'] > field.data:
            raise validators.ValidationError(_l('level needs to be bigger or equal to start level'))


class WMTSForm(RasterSourceForm):
    layer = None
    srs = None


class WMSForm(RasterSourceForm):
    version = SelectField(_l('wms_version'), choices=[('1.1.1', '1.1.1'), ('1.3.0', '1.3.0')],
        validators=[validators.Required()])


class WFSForm(Form):
    host = TextField(_l('wfs_host'), [validators.Required()])
    url = TextField(_l('wfs_url'), [validators.Required()])
    geometry = TextField(_l('wfs_geometry'), [validators.Required()], default="the_geom")
    layer = TextField(_l('wfs_layer'), [validators.Required()])
    name = TextField(_l('wfs_name'), [validators.Required(), validators.Regexp('[a-zA-Z0-9_-]+$')])

    srs = SelectField(_l('wfs_srs'), [validators.Required()], choices=[('EPSG:3857', 'EPSG:3857')])

    ns_prefix = TextField(_l('wfs_ns_prefix'))
    ns_uri = TextField(_l('wfs_ns_uri'))

    search_property = TextField(_l('wfs_search_property'))
    max_features = IntegerField(_l('wfs_max_features'), [validators.Required()])

    username = TextField(_l('rvectorsource_username'))
    password = PasswordField(_l('vectorsource_password'))
    is_protected = BooleanField(_l('vectorsoure_protected'))


