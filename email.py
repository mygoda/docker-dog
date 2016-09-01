# -*- coding: utf-8 -*-
import sys
import logging

import ewsclient
import ewsclient.monkey
import suds.client
from suds.transport.https import WindowsHttpAuthenticated


reload(sys)
sys.setdefaultencoding("utf-8")

logger = logging.getLogger(__name__)


class Email():
    '''
    eg:
        e = Email()
        e.send(["xx@qq.com",xx@qq.com"], '邮件标题', '邮件内容')
    '''

    def __init__(self, domain, username, password):
        transport = WindowsHttpAuthenticated(username=username,
                                             password=password)
        self.client = suds.client.Client("https://%s/EWS/Services.wsdl" % domain,
                                         transport=transport,
                                         plugins=[ewsclient.AddService()])
    def send(self, to_list, subject, content):
        email_address = u'''<t:Mailbox><t:EmailAddress>%s</t:EmailAddress></t:Mailbox>'''
        to = "".join([email_address % email for email in to_list])
        if not isinstance(subject, unicode):
            subject = unicode(subject, "utf-8")
        if not isinstance(content, unicode):
            content = unicode(content, "utf-8")

        xml = u'''<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
                  <soap:Body>
                    <CreateItem MessageDisposition="SendAndSaveCopy" xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
                      <SavedItemFolderId>
                        <t:DistinguishedFolderId Id="sentitems" />
                      </SavedItemFolderId>
                      <Items>
                        <t:Message>
                          <t:ItemClass>IPM.Note</t:ItemClass>
                          <t:Subject><![CDATA[%s]]></t:Subject>
                          <t:Body BodyType="HTML"><![CDATA[%s]]></t:Body>
                          <t:ToRecipients>
                            %s
                          </t:ToRecipients>
                        </t:Message>
                      </Items>
                    </CreateItem>
                  </soap:Body>
                </soap:Envelope>''' % (subject, content, to)
        logger.info(xml)
        try:
            self.client.service.CreateItem(__inject={u'msg': xml})
            return True
        except Exception, e:
            logger.exception(u"邮件发送失败！%s %s %s" % (to_list, subject, content))
            return False