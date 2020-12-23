from ruqqus.helpers.base36 import *
from ruqqus.helpers.security import *
from sqlalchemy import *
from sqlalchemy.orm import relationship
from ruqqus.__main__ import Base, cache
from .mix_ins import *
import time


class ModAction(Base, Stndrd, Age_times):
    __tablename__ = "modactions"
    id = Column(BigInteger, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    board_id = Column(Integer, ForeignKey("boards.id"))
    kind = Column(String(32))
    target_user_id = Column(Integer, ForeignKey("users.id"), default=0)
    target_submission_id = Column(Integer, ForeignKey("submissions.id"), default=0)
    target_comment_id = Column(Integer, ForeignKey("comments.id"), default=0)
    #targetLodge = Column(Integer, ForeignKey("lodges.id"), default=0)
    #targetRule = Column(Boolean, ForeignKey("rules.id"), default=False)
    note=Column(String(64), default=None)
    created_utc = Column(Integer, default=0)


    user = relationship("User", lazy="joined", primaryjoin="User.id==ModAction.user_id")
    target_user = relationship("User", lazy="joined", primaryjoin="User.id==ModAction.target_user_id")
    board = relationship("Board", lazy="joined")
    #target_lodge = relationship("Lodge", lazy="joined")
    #target_rule = relationship("Rule", lazy="joined")
    target_post = relationship("Submission", lazy="joined")
    target_comment = relationship("Comment", lazy="joined")


    def __init__(self, *args, **kwargs):
        if "created_utc" not in kwargs:
            kwargs["created_utc"] = int(time.time())

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<ModAction(id={self.base36id})>"

    @property
    def actiontype(self):
        return ACTIONTYPES[self.kind]

    @property
    def str(self):
        output =  self.actiontype["str"].format(self=self)
        if self.note:
            output +=f" <i>({self.note})</i>"

        return output

    @property
    def icon(self):
        return self.actiontype['icon']

    @property
    def permalink(self):
        return f"{self.board.permalink}/mod/log/{self.base36id}"
    
    


ACTIONTYPES={
    "kick_post":{
        "str":'kicked post <a href="{self.target_post.url}" target="_blank">{self.target_post.title}</a>',
        "icon":"fa-sign-out fa-flip-horizontal text-danger"
    },
    "approve_post":{
        "str":'approved post <a href="{self.target_post.url}" target="_blank">{self.target_post.title}</a>',
        "icon":"fa-check text-success"
    },    
    "yank_post":{
        "str":'yanked post <a href="{self.target_post.url}" target="_blank">{self.target_post.title}</a>',
        "icon":"fa-hand-lizard text-muted"
    },
    "exile_user":{
        "str":'exiled user <a href="{self.target_user.permalink}" target="_blank">@{self.target_user.username}</a>',
        "icon":"fa-user-slash text-danger"
    },
    "unexile_user":{
        "str":'un-exiled user <a href="{self.target_user.permalink}" target="_blank">@{self.target_user.username}</a>',
        "icon": "fa-user-slash text-muted"
    },
    "contrib_user":{
        "str":'added contributor <a href="{self.target_user.permalink}" target="_blank">@{self.target_user.username}</a>',
        "icon": "fa-user-check text-info"
    },
    "uncontrib_user":{
        "str":'removed contributor <a href="{self.target_user.permalink}" target="_blank">@{self.target_user.username}</a>',
        "icon": "fa-user-check text-muted"
    },
    "herald_comment":{
        "str":'heralded their <a href="{self.target_comment.permalink}" target="_blank">comment</a>',
        "icon": "fa-crown text-warning"
    },
    "herald_post":{
        "str":'heralded their post <a href="{self.target_post.permalink}" target="_blank">{self.target_post.title}</a>',
        "icon": "fa-crown text-warning"
    },
    "unherald_comment":{
        "str":'un-heralded their <a href="{self.target_comment.permalink}" target="_blank">comment</a>',
        "icon": "fa-crown text-muted"
        },
    "unherald_post":{
        "str":'un-heralded their post <a href="{self.target_post.permalink}" target="_blank">{self.target_post.title}</a>',
        "icon": "fa-crown text-muted"
    },
    "pin_comment":{
        "str":'pinned a <a href="{self.target_comment.permalink}" target="_blank">comment</a>',
        "icon":"fa-thumbtack fa-rotate--45 text-info",
    },
    "unpin_comment":{
        "str":'un-pinned a <a href="{self.target_comment.permalink}" target="_blank">comment</a>',
        "icon":"fa-thumbtack fa-rotate--45 text-muted",
    },
    "pin_post":{
        "str":'pinned post <a href="{self.target_post.url}" target="_blank">{self.target_post.title}</a>',
        "icon":"fa-thumbtack fa-rotate--45 text-info",
    },
    "unpin_post":{
        "str":'un-pinned post <a href="{self.target_post.url}" target="_blank">{self.target_post.title}</a>',
        "icon":"fa-thumbtack fa-rotate--45 text-muted",
    },
    "invite_mod":{
        "str":'invited Guildmaster <a href="{self.target_user.permalink}" target="_blank">@{self.target_user.username}</a>',
        "icon":"fa-user-crown text-info"
    },
    "uninvite_mod":{
        "str":'rescinded Guildmaster invitation to <a href="{self.target_user.permalink}" target="_blank">@{self.target_user.username}</a>',
        "icon":"fa-user-crown text-muted"
    },
    "accept_mod_invite":{
        "str":'accepted Guildmaster invitation',
        "icon":"fa-user-crown text-warning"
    },
    "remove_mod":{
        "str":'removed Guildmaster <a href="{self.target_user.permalink}" target="_blank">@{self.target_user.username}</a>',
        "icon":"fa-user-crown text-danger"
    },
    "dethrone_self":{
        "str":'stepped down as guildmaster',
        "icon":"fa-user-crown text-danger"
    },
    "add_mod":{
        "str":'added Guildmaster <a href="{self.target_user.permalink}" target="_blank">@{self.target_user.username}</a>',
        "icon":"fa-user-crown text-success"
    },
    "update_settings":{
        "str":'updated setting',
        "icon":"fa-cog text-info"
    },
    "update_appearance":{
        "str":'updated appearance',
        "icon":"fa-palette text-info"
    },
    "set_nsfw":{
        "str":'set nsfw on post <a href="{self.target_post.url}" target="_blank">{self.target_post.title}</a>',
        "icon":"fa-eye-evil text-danger"
    },
    "unset_nsfw":{
        "str":'unset nsfw on post <a href="{self.target_post.url}" target="_blank">{self.target_post.title}</a>',
        "icon":"fa-eye-evil text-muted"
    },
    "set_nsfl":{
        "str":'set nsfl on post <a href="{self.target_post.url}" target="_blank">{self.target_post.title}</a>',
        "icon":"fa-skull text-black"
    },
    "unset_nsfl":{
        "str":'unset nsfl on post <a href="{self.target_post.url}" target="_blank">{self.target_post.title}</a>',
        "icon":"fa-skull text-muted"
    }
}