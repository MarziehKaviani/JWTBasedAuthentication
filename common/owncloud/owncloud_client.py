import six
from owncloud import ET, Client, HTTPResponseError, ShareInfo


class CustomClient(Client):
    def custom_params(self, path, **kwargs):
        """Removing name from original share_file_with_link method.
        """
        perms = kwargs.get('perms', None)
        public_upload = kwargs.get('public_upload', 'false')
        password = kwargs.get('password', None)
        expire = kwargs.get('expire', None)
        hide_download = kwargs.get('hide_download', None)

        path = self._normalize_path(path)
        post_data = {
            'shareType': self.OCS_SHARE_TYPE_LINK,
            'path': self._encode_string(path),
        }
        if (public_upload is not None) and (isinstance(public_upload, bool)):
            post_data['publicUpload'] = str(public_upload).lower()
        if isinstance(password, six.string_types):
            post_data['password'] = password
        if expire:
            post_data['expireDate'] = expire
        if perms:
            post_data['permissions'] = perms
        if hide_download:
            post_data['hideDownload'] = hide_download

        res = self._make_ocs_request(
            'POST',
            self.OCS_SERVICE_SHARE,
            'shares',
            data=post_data
        )
        if res.status_code == 200:
            tree = ET.fromstring(res.content)
            self._check_ocs_status(tree)
            data_el = tree.find('data')
            return ShareInfo(
                {
                    'id': data_el.find('id').text,
                    'path': path,
                    'url': data_el.find('url').text,
                    'token': data_el.find('token').text,
                }
            )
        raise HTTPResponseError(res)
