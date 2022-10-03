def unread(request):

    try:
        unread = request.user.profile.messages.all().filter(is_read=False).count()

        return {'unread': unread}
    except:
        return ''
