from restfulpy.messaging.models import Email


class ResetPasswordEmail(Email):
    __mapper_args__ = {
        'polymorphic_identity': 'reset_password_email'
    }

    template_filename = 'reset_password.mako'


class ActivationEmail(Email):
    __mapper_args__ = {
        'polymorphic_identity': 'activation_email'
    }
    template_filename = 'activation.mako'


class FeedbackSubmissionNuemdEmail(Email):
    __mapper_args__ = {
        'polymorphic_identity': 'feedback_submission_nuemd_email'
    }
    template_filename = 'feedback_submission_nuemd.mako'


class FeedbackSubmissionUserEmail(Email):
    __mapper_args__ = {
        'polymorphic_identity': 'feedback_submission_user_email'
    }
    template_filename = 'feedback_submission_user.mako'
